from django.db import models
from django.utils.translation import ugettext as _

from extended_models.models import SerializableModel

class School(SerializableModel):
    jp_name = models.CharField(max_length=100, unique=True)
    en_name = models.CharField(max_length=100)
    en_short_name = models.CharField(max_length=30)
    jp_short_name = models.CharField(max_length=30)

    def normalize(self):
        return {
            'id': self.pk,
            'jp_name': self.jp_name,
            'en_name': self.en_name,
            'en_short_name': self.en_short_name,
            'jp_short_name': self.jp_short_name
        }

class Teacher(SerializableModel):
    jp_first_name = models.CharField(max_length=100)
    jp_last_name = models.CharField(max_length=100)
    en_first_name = models.CharField(max_length=100)
    en_last_name = models.CharField(max_length=100)
    school = models.ForeignKey(School)

    def normalize(self):
        return {
            'id': self.pk,
            'jp_first_name': self.jp_first_name,
            'jp_last_name': self.jp_last_name,
            'en_first_name': self.en_first_name,
            'en_last_name': self.en_last_name
        }

class Period(SerializableModel):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def normalize(self):
        return {
            'id': self.pk,
            'start_time': self.start_time.strftime("%H:%M"),
            'end_time': self.end_time.strftime("%H:%M")
        }

class Subject(SerializableModel):
    TERM_CHOICES = (
        ('SP', _('spring')),
        ('AU', _('autumn')),
        ('SU', _('summer')),
        ('WI', _('winter')),
        ('AY', _('all_year')),
        (None, _('none'))
    )

    jp_name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200)
    school = models.ForeignKey(School)
    net_portal_id = models.CharField(max_length=30, unique=True)
    term = models.CharField(max_length=2, choices=TERM_CHOICES, null=True)
    jp_description = models.TextField(blank=True, default="")
    en_description = models.TextField(blank=True, default="")
    teachers = models.ManyToManyField(Teacher)
    year = models.IntegerField()

    def normalize(self):
        if hasattr(self, 'classes'):
            r = {'classes': [c.normalize() for c in self.classes]}
        else:
            r = {}
        r.update({
            'id': self.pk,
            'jp_name': self.jp_name,
            'en_name': self.en_name,
            'school': self.school.normalize(),
            'net_portal_id': self.net_portal_id,
            'term': self.get_term_display(),
            'jp_description': self.jp_description,
            'en_description': self.en_description,
            'teachers': [t.normalize() for t in self.teachers.all()],
            'year': self.year
        })
        return r

class Building(SerializableModel):
    jp_name = models.CharField(max_length=50, unique=True)
    en_name = models.CharField(max_length=50, unique=True)

    def normalize(self):
        return {
            'id': self.pk,
            'jp_name': self.jp_name,
            'en_name': self.en_name
        }


class Classroom(SerializableModel):
    building = models.ForeignKey(Building, null=True)
    jp_name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    info = models.CharField(max_length=50, null=True)

    def normalize(self):
        return {
            'id': self.pk,
            'building': self.building.normalize() if self.building else None,
            'jp_name': self.jp_name,
            'en_name': self.en_name,
            'info': self.info
        }

class Class(SerializableModel):
    WEEKDAYS = ((None, _('none')),) + tuple(
        (day, _(day)) for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    )
    subject = models.ForeignKey(Subject)
    day_of_week = models.CharField(max_length=3, choices=WEEKDAYS, null=True)
    start_period = models.ForeignKey(Period, null=True, related_name="start_period")
    end_period = models.ForeignKey(Period, null=True, related_name="end_period")
    classroom = models.ForeignKey(Classroom, null=True)

    def normalize(self):
        return {
            'id': self.pk,
            'day_of_week': self.day_of_week,
            'start_period': self.start_period.normalize() if self.start_period else None,
            'end_period': self.end_period.normalize() if self.end_period else None,
            'classroom': self.classroom.normalize() if self.classroom else None
        }
