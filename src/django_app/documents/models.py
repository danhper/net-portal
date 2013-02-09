from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from courses.models import Teacher, Subject
from extended_models.models import SerializableModel
from api import CourseNaviAPI, NetPortalException

class DocumentFolder(SerializableModel):
    TYPE_CHOICES = (('news', 'news'), ('notes', 'notes'))
    doctype = models.CharField(max_length=5, choices=TYPE_CHOICES)
    subject = models.ForeignKey(Subject)
    year = models.IntegerField()
    waseda_id = models.CharField(max_length=20)
    title = models.CharField(max_length=100)

    @staticmethod
    def get_from_api(username, password, subject, year):
        api = CourseNaviAPI()
        if not api.login(username, password):
            raise NetPortalException("invalid username/password")
        api.login_cnavi()
        waseda_id = "{0}{1}".format(year, subject.net_portal_id)
        return api.get_subject_documents(waseda_id, subject.waseda_folder_id)

    @staticmethod
    def add_folders(folders_objects):
        document_folders = Document.objects.prefetch_related().filter(waseda_id__in=map(lambda v: v['waseda_id'], folders_objects))
        new_folders = []
        for folder in folders_objects:
            try:
                f = document_folders.get(waseda_id=folder['waseda_id'])
            except ObjectDoesNotExist:
                folder_data = dict(folder)
                del folder_data['documents']
                f = DocumentFolder(**folder_data)
                new_folders.append(f)
            folder_docs = f.document_set.filter(waseda_id__in=map(lambda v: v['waseda_id'], folder['documents']))
            # teachers = Teacher.objects.filter(first_name__)
            for d in folder['documents']:
                if not folder_docs.filter(waseda_id=d['waseda_id']).exists():
                    pass


class Document(SerializableModel):
    TYPE_CHOICES = (('news', 'news'), ('note', 'note'), ('report', 'report'))
    title = models.CharField(max_length=100)
    doctype = models.CharField(max_length=5, choices=TYPE_CHOICES)
    display_start = models.DateTimeField(default=datetime.now)
    display_end = models.DateTimeField(null=True)
    uploader = models.ForeignKey(Teacher)
    files = models.FilePathField()
    waseda_id = models.CharField(max_length=20, blank=True)
    folder = models.ForeignKey(DocumentFolder)

    class Meta:
        ordering = ['display_start']


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
