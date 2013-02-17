from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import get_language

from datetime import datetime

from courses.models import Teacher, Subject
from extended_models.models import SerializableModel
from api import CourseNaviAPI, NetPortalException

class DocumentFolderManager(models.Manager):
    def add_folders(self, folders_objects, subject):
        db_folders = DocumentFolder.objects.filter(waseda_id__in=[f['waseda_id'] for f in folders_objects])
        folders = {f.waseda_id: f for f in db_folders}
        new_folders = []
        for f in folders_objects:
            if not f['waseda_id'] in folders:
                new_folders.append(DocumentFolder(title=f['title'], waseda_id=f['waseda_id'], doctype=f['doctype'], subject=subject))
        DocumentFolder.objects.bulk_create(new_folders)
        folders.update({f.waseda_id: f for f in new_folders})

        documents = []
        for f in folders_objects:
            for d in f['documents']:
                d['folder'] = folders[f['waseda_id']]
                documents.append(d)

        Document.add_documents(documents, subject)

class DocumentFolder(SerializableModel):
    TYPE_CHOICES = (('news', 'news'), ('notes', 'notes'))
    doctype = models.CharField(max_length=5, choices=TYPE_CHOICES)
    subject = models.ForeignKey(Subject)
    year = models.IntegerField()
    waseda_id = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    explanation = models.TextField(null=True)
    files = models.FilePathField(null=True)

    objects = DocumentFolderManager()

    @staticmethod
    def get_from_api(username, password, subject, year):
        api = CourseNaviAPI()
        if not api.login(username, password):
            raise NetPortalException("invalid username/password")
        api.login_cnavi()
        waseda_id = "{0}{1}".format(year, subject.waseda_id)
        return api.get_subject_documents(waseda_id, subject.waseda_folder_id)


class DocumentManager(models.Manager):
    def add_documents(self, documents_objects, subject):
        db_docs = Document.objects.filter(waseda_id__in=[d['waseda_id'] for d in documents_objects])
        documents = {d.waseda_id: d for d in db_docs}
        names = {(d['uploader_first_name'], d['uploader_last_name']) for d in documents_objects}
        get_name = lambda t: t.ja_last_name, t.ja_first_name if get_language() == 'ja' else t.en_last_name, t.en_first_name
        db_teachers = {get_name(t): t for t in Teacher.objects.get_from_names(subject.school, names)}
        new_documents = []
        for d in documents_objects:
            if d['waseda_id'] not in documents:
                teacher = teachers[(d['uploader_last_name'], d['uploader_first_name'])]
                new_doc = Document(title=d['title'], display_start=d['display_start'], display_end=d['display_end'], uploader=teacher, waseda_id=waseda_id, doctype=doctype)
                new_documents.append(new_doc)
        Document.objects.bulk_create(new_documents)

class Document(SerializableModel):
    class Meta:
        ordering = ['display_start']

    TYPE_CHOICES = (('news', 'news'), ('note', 'note'), ('report', 'report'))
    title = models.CharField(max_length=100)
    doctype = models.CharField(max_length=5, choices=TYPE_CHOICES)
    display_start = models.DateTimeField(default=datetime.now)
    display_end = models.DateTimeField(null=True)
    uploader = models.ForeignKey(Teacher)
    files = models.FilePathField(null=True)
    waseda_id = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, null=True)
    folder = models.ForeignKey(DocumentFolder, null=True)


class Report(Document):
    SUBMIT_METHOD_CHOICES = (('attachment', 'attachment'), ('main_text', 'main_text'), ('any', 'any'))
    submit_method = models.CharField(max_length=10)
    deadline = models.DateTimeField()
    show_results = models.BooleanField(default=False)
    temporary_save = models.BooleanField(default=True)
    results_view_start = models.DateTimeField(null=True)
    results_view_end = models.DateTimeField(null=True)
    public = models.BooleanField(default=False)
    late_submit = models.BooleanField(default=False)
    latest_submit_date = models.DateTimeField(null=True)
    comments_active = models.BooleanField(default=True)
    files_number_limit = models.IntegerField(null=True)
    accepted_file_extensions = models.CharField(max_length=255)
