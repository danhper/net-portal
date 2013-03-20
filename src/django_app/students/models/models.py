from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import base64
import rsa

from courses.models import Subject, Class, Term, TermPeriod
from documents.models import Report, Document
from extended_models.models import SerializableModel, SerializableList
from managers import RegistrationManager


class StudentProfile(SerializableModel):
    """Class to use as user profile"""

    class Meta:
        app_label = "students"

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
        to_add = Subject.objects.filter(waseda_id__in=subjects.keys())
        classes = Class.objects.select_related('subject', 'term').filter(subject__in=to_add)
        offset = self.subjects.count()
        registrations = []
        years = set()
        for subject in to_add:
            folder_id = subjects[subject.waseda_id]["folder_id"]
            for year in subjects[subject.waseda_id]["years"]:
                r = SubjectRegistration(subject=subject, profile=self, order=offset + len(registrations))
                r.year = year
                registrations.append(r)
                years.add(year)
            if not subject.waseda_folder_id:
                subject.waseda_folder_id = folder_id
                subject.save()

        term_periods = TermPeriod.objects.select_related().filter(year__in=years)
        for registration in registrations:
            terms = [class_obj.term for class_obj in classes.filter(subject=registration.subject)]
            term = Term.get_max_term(terms)
            registration.period = term_periods.get(year=registration.year, term=term)

        SubjectRegistration.objects.bulk_create(registrations)

    def get_subjects(self):
        registrations = SubjectRegistration.objects.get_with_related(profile=self)

        return SerializableList(registrations)


class SubjectRegistration(SerializableModel):
    class Meta:
        app_label = "students"

    subject = models.ForeignKey(Subject)
    profile = models.ForeignKey(StudentProfile)
    order = models.IntegerField()
    period = models.ForeignKey(TermPeriod)
    favorite = models.BooleanField(default=False)

    objects = RegistrationManager()

    def normalize(self):
        return {
            'id': self.pk,
            'subject': self.subject.normalize(),
            'order': self.order,
            'period': self.period.normalize(),
            'favorite': self.favorite
        }

    def update(self, args):
        order = args.get('order', self.order)
        if order != self.order:
            SubjectRegistration.objects.reorder(self.order, order)
            self.order = order
        self.favorite = args.get('favorite', self.favorite)
        self.save()


class DocumentStatus(SerializableModel):
    class Meta:
        app_label = "students"
    user = models.ForeignKey(StudentProfile)
    document = models.ForeignKey(Document)


class ReportSubmission(SerializableModel):
    class Meta:
        app_label = "students"
    document_status = models.ForeignKey(DocumentStatus)
