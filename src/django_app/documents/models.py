from django.db import models
from extended_models.models import SerializableModel
from courses.models import Teacher
import datetime

class Document(SerializableModel):
    TYPE_CHOICES = (('news', 'news'), ('work', 'work'), ('report', 'report'))
    title = models.CharField(max_length=100)
    doctype = models.CharField(max_length=5, choices=TYPE_CHOICES)
    display_start = models.DateTimeField(default=datetime.now)
    display_end = models.DateTimeField(null=True)
    uploader = models.ForeignKey(Teacher)
    files = models.FilePathField()

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


class LectureDocuments(SerializableModel):
    documents = models.ManyToManyField(Document)
    year = models.IntegerField()
