from django.db import models
from django.utils.translation import ugettext as _

class School(models.Model):
    jp_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    en_short_name = models.CharField(max_length=30)
    jp_short_name = models.CharField(max_length=30)


class Teacher(models.Model):
    jp_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    school = models.ForeignKey(School)


class Period(models.Model):
    pass


class Subject(models.Model):
    TERM_CHOICES = (
        ('SP', _('spring')),
        ('AU', _('autumn'))
    )

    jp_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    net_portal_key = models.IntegerField()
    term = models.CharField(max_length=2, choices=TERM_CHOICES)
    classroom = models.CharField(max_length=10)
    periods = models.ManyToManyField(Period)
    description = models.TextField()
