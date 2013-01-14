from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

import base64
import rsa

from courses.models import Subject, Class


class StudentProfile(models.Model):
    """Class to use as user profile"""
    user = models.OneToOneField(User)
    encrypted_password = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, through='SubjectRegistration')
    jp_first_name = models.CharField(max_length=100)
    jp_last_name = models.CharField(max_length=100)
    en_first_name = models.CharField(max_length=100)
    en_last_name = models.CharField(max_length=100)
    student_nb = models.CharField(max_length=15)

    @property
    def plain_password(self):
        with open(settings.RSA["private_key_path"], "r") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        encrypted_password = base64.b64decode(self.encrypted_password)
        return rsa.decrypt(encrypted_password, private_key)

    """Takes plain password and set encrypted password on the model."""
    def set_password(self, plain_password):
        with open(settings.RSA["public_key_path"], "r") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        encrypted_password = rsa.encrypt(str(plain_password), public_key)
        b64_encrypted_password = base64.b64encode(encrypted_password)
        self.encrypted_password = b64_encrypted_password

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

    def get_subjects(self):
        registrations = SubjectRegistration.objects.select_related().filter(profile=self)
        classes = Class.objects.select_related().filter(subject__in=[r.subject for r in registrations])

        for registration in registrations:
            registration.subject.classes = [class_obj for class_obj in classes if class_obj.subject == registration.subject]

        return registrations

class SubjectRegistration(models.Model):
    subject = models.ForeignKey(Subject)
    profile = models.ForeignKey(StudentProfile)
    order = models.IntegerField()
    year = models.IntegerField()


class StudentManager(models.Manager):
    def create_with_info(self, username, password, info, subjects):
        p = User.objects.create(username=username, password=password).get_profile()
        p.__dict__.update(**info)
        p.add_subjects(subjects)
        p.save()

StudentManager().contribute_to_class(User, 'students')


@receiver(pre_save, sender=User)
def prepare_user_creation(sender, instance, **kwargs):
    # only run on creation, not on update
    if instance.pk is not None:
        return

    if not instance.username or not instance.password:
        raise ValueError("A instance needs a username and a password")

    # check if password is hashed. need to adapt for other hash
    if instance.password.startswith("pbkdf2_sha256") and instance.password.endswith("="):
        raise ValueError("Need unhashed password to create instance. Current: {0}.".format(instance.password))

    profile = StudentProfile()
    profile.set_password(instance.password)

    # bind temporary profile while no pk
    instance.profile = profile

    if not instance.email:
        instance.email = instance.username

    # insert hashed password in database
    instance.password = make_password(instance.password)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # only run on creation, not on update
    if not created:
        return

    instance.profile.user = instance
    instance.profile.save()
    instance.profile = None
