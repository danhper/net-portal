from django.db import models
from django.utils.translation import ugettext as _

class School(models.Model):
    jp_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    en_short_name = models.CharField(max_length=30)
    jp_short_name = models.CharField(max_length=30)


class Teacher(models.Model):
    jp_first_name = models.CharField(max_length=100)
    jp_last_name = models.CharField(max_length=100)
    en_first_name = models.CharField(max_length=100)
    en_last_name = models.CharField(max_length=100)
    school = models.ForeignKey(School)

class Period(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

class Subject(models.Model):
    TERM_CHOICES = (
        ('SP', _('spring')),
        ('AU', _('autumn')),
        ('AY', _('all_year'))
    )

    jp_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    net_portal_id = models.IntegerField()
    term = models.CharField(max_length=2, choices=TERM_CHOICES)
    jp_description = models.TextField(blank=True, default="")
    en_description = models.TextField(blank=True, default="")
    teachers = models.ManyToMany(Teacher)

class Building(models.Model):
    pass

class Classroom(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=10)

class Class(models.Model):
    WEEKDAYS = (
        (day, _(day)) for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    )
    subject = models.ForeignKey(Subject)
    days_of_week = models.CharField(max_length=3, choices=WEEKDAYS)
    start_period = models.ForeignKey(Period)
    end_period = models.ForeignKey(Period)
    classroom = models.ForeignKey(Classroom)
