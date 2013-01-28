from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

import base64
import rsa

from courses.models import Subject, Class, Term, TermPeriod
from extended_models.models import SerializableModel, SerializableList


class StudentProfile(SerializableModel):
    """Class to use as user profile"""
    user = models.OneToOneField(User)
    encrypted_password = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, through='SubjectRegistration')
    ja_first_name = models.CharField(max_length=100)
    ja_last_name = models.CharField(max_length=100)
    en_first_name = models.CharField(max_length=100)
    en_last_name = models.CharField(max_length=100)
    student_nb = models.CharField(max_length=15)

    def normalize(self):
        return {
            'id': self.pk,
            'ja_first_name': self.ja_first_name,
            'ja_last_name': self.ja_last_name,
            'en_first_name': self.en_first_name,
            'en_last_name': self.en_last_name,
            'student_nb': self.student_nb,
            'email': self.user.email
        }

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
        to_add = Subject.objects.filter(net_portal_id__in=subjects.keys())
        classes = Class.objects.select_related('subject', 'term').filter(subject__in=to_add)
        offset = self.subjects.count()
        registrations = []
        years = set()
        for subject in to_add:
            folder_id = subjects[subject.net_portal_id]["folder_id"]
            for year in subjects[subject.net_portal_id]["years"]:
                r = SubjectRegistration(subject=subject, profile=self, order=offset + len(registrations), net_portal_folder_id=folder_id)
                r.year = year
                registrations.append(r)
                years.add(year)

        term_periods = TermPeriod.objects.select_related().filter(year__in=years)
        for registration in registrations:
            terms = [class_obj.term for class_obj in classes.filter(subject=registration.subject)]
            term = Term.get_max_term(terms)
            registration.period = term_periods.get(year=r.year, term=term)

        SubjectRegistration.objects.bulk_create(registrations)

    def get_subjects(self):
        registrations = SubjectRegistration.objects.get_with_related(profile=self)

        return SerializableList(registrations)

class RegistrationManager(models.Manager):
    def get_with_related(self, **kwargs):
        cr = ['classes', 'classes__term', 'classes__start_period']
        cr += ['classes__end_period', 'classes__classroom']
        cr += ['classes__classroom__building', 'classes__subject']
        tr = ['teachers', 'teachers__school']
        subject_related = ['subject__{0}'.format(v) for v in cr + tr]
        return SubjectRegistration.objects.select_related().prefetch_related(*subject_related).filter(**kwargs)


class SubjectRegistration(SerializableModel):
    subject = models.ForeignKey(Subject)
    profile = models.ForeignKey(StudentProfile)
    order = models.IntegerField()
    period = models.ForeignKey(TermPeriod)
    net_portal_folder_id = models.IntegerField()
    favorite = models.BooleanField(default=False)

    objects = RegistrationManager()

    def normalize(self):
        return {
            'id': self.pk,
            'subject': self.subject.normalize(),
            'order': self.order,
            'period': self.period.normalize(),
            'net_portal_folder_id': self.net_portal_folder_id
        }

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
        # need to check if called from CLI
        pass
        # raise ValueError("Need unhashed password to create instance. Current: {0}.".format(instance.password))
    else:
        profile = StudentProfile()
        profile.set_password(instance.password)

        # bind temporary profile while no pk
        instance.profile = profile
        # insert hashed password in database
        instance.password = make_password(instance.password)

    if not instance.email:
        instance.email = instance.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # only run on creation, not on update
    if not created:
        return

    if hasattr(instance, 'profile'):
        instance.profile.user = instance
        instance.profile.save()
        instance.profile = None
