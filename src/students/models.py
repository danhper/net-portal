from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from courses.models import Subject
import base64
import rsa


class StudentProfile(models.Model):
    """Class to use as user profile"""
    user = models.OneToOneField(User)
    encrypted_password = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, through='SubjectRegistration')

    @property
    def plain_password(self):
        with open(settings.RSA["private_key_path"], "r") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        encrypted_password = base64.b64decode(self.encrypted_password)
        return rsa.decrypt(encrypted_password, private_key)

    def add_subjects(self, subjects):
        if type(subjects) is not dict or any(type(v) is not list for v in subjects.values()):
            raise ValueError("Subjects should be a dict with net_portal_id as \
                key and a list of the years during which the subject was take as value. {0}".format(type(subjects)))
        to_add = Subject.objects.filter(net_portal_id__in=subjects.keys())
        offset = self.subjects.count()
        relations = []
        for (i, subject) in enumerate(to_add):
            year = subjects[subject.net_portal_id].pop()
            r = SubjectRegistration(subject=subject, profile=self, order=offset + i, year=year)
            relations.append(r)
        SubjectRegistration.objects.bulk_create(relations)

class SubjectRegistration(models.Model):
    subject = models.ForeignKey(Subject)
    profile = models.ForeignKey(StudentProfile)
    order = models.IntegerField()
    year = models.IntegerField()

class StudentManager(models.Manager):
    def create_with_subjects(self, username, password, subjects):
        p = User.objects.create(username=username, password=password).get_profile()
        p.add_subjects(subjects)
        p.save()

StudentManager().contribute_to_class(User, 'students')


@receiver(pre_save, sender=User)
def prepare_user_save(sender, instance, **kwargs):
    if instance.pk is not None:
        return

    if not instance.username or not instance.password:
        raise ValueError("A instance needs a username and a password")

    if instance.password.startswith("pbkdf2_sha256") and instance.password.endswith("="):
        raise ValueError("Need unhashed password to create instance. Current: {0}.".format(instance.password))

    if type(instance.password) != 'str':
        instance.password = str(instance.password)

    if not instance.email:
        instance.email = instance.username

    with open(settings.RSA["public_key_path"], "r") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypted_password = rsa.encrypt(instance.password, public_key)
    b64_encrypted_password = base64.b64encode(encrypted_password)

    # temporary field for encrypted password
    instance.encrypted_password = b64_encrypted_password

    # insert hashed password in database
    instance.password = make_password(instance.password)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile, new = StudentProfile.objects.get_or_create(user=instance, encrypted_password=instance.encrypted_password)
    instance.encrypted_password = None
