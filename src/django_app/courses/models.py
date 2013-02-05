from django.db import models

from extended_models.models import SerializableModel

from api import CourseNaviAPI, NetPortalException

class School(SerializableModel):
    ja_name = models.CharField(max_length=100, unique=True)
    en_name = models.CharField(max_length=100)
    en_short_name = models.CharField(max_length=30)
    ja_short_name = models.CharField(max_length=30)

    def normalize(self):
        return {
            'id': self.pk,
            'ja_name': self.ja_name,
            'en_name': self.en_name,
            'en_short_name': self.en_short_name,
            'ja_short_name': self.ja_short_name
        }

class Teacher(SerializableModel):
    ja_first_name = models.CharField(max_length=100)
    ja_last_name = models.CharField(max_length=100)
    en_first_name = models.CharField(max_length=100)
    en_last_name = models.CharField(max_length=100)
    school = models.ForeignKey(School)

    def normalize(self):
        return {
            'id': self.pk,
            'ja_first_name': self.ja_first_name,
            'ja_last_name': self.ja_last_name,
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
    ja_name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200)
    school = models.ForeignKey(School)
    net_portal_id = models.CharField(max_length=30, unique=True)
    ja_description = models.TextField(blank=True, default="")
    en_description = models.TextField(blank=True, default="")
    teachers = models.ManyToManyField(Teacher)
    year = models.IntegerField()

    @staticmethod
    def get_from_api(username, password, category='attending', get_user_info=False):
        api = CourseNaviAPI()
        if not api.login(username, password):
            raise NetPortalException("invalid username/password")
        api.login_cnavi()
        subjects = api.get_subjects(category)
        return subjects if not get_user_info else (subjects, api.user_info)

    def normalize(self):
        return {
            'id': self.pk,
            'ja_name': self.ja_name,
            'en_name': self.en_name,
            'school': self.school.normalize(),
            'net_portal_id': self.net_portal_id,
            'ja_description': self.ja_description,
            'en_description': self.en_description,
            'teachers': [t.normalize() for t in self.teachers.all()],
            'year': self.year,
            'classes': [c.normalize() for c in self.classes.all()]
        }


class Building(SerializableModel):
    ja_name = models.CharField(max_length=50, unique=True)
    en_name = models.CharField(max_length=50, unique=True)

    def normalize(self):
        return {
            'id': self.pk,
            'ja_name': self.ja_name,
            'en_name': self.en_name
        }


class Classroom(SerializableModel):
    building = models.ForeignKey(Building, null=True)
    ja_name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    info = models.CharField(max_length=50, null=True)

    def normalize(self):
        return {
            'id': self.pk,
            'building': self.building.normalize() if self.building else None,
            'ja_name': self.ja_name,
            'en_name': self.en_name,
            'info': self.info
        }


class Term(SerializableModel):
    TERM_CHOICES = (
        ('FI', 'first'),
        ('AU', 'autumn'),
        ('SU', 'summer'),
        ('SN', 'second'),
        ('WI', 'winter'),
        ('SP', 'spring'),
        ('AY', 'all_year'),
        ('OT', 'other')
    )

    name = models.CharField(max_length=2, choices=TERM_CHOICES)
    sort_order = models.IntegerField()

    @staticmethod
    def get_max_term(terms):
        if len(terms) == 1:
            return terms[0]
        if len(terms) == 2:
            names = [term.name for term in terms]
            if 'FI' in names and 'SN' in names:
                return Term.objects.get(name='AY')
        return max(terms, key=lambda t: t.sort_order)

    def normalize(self):
        return {
            'id': self.pk,
            'name': self.get_name_display()
        }


class TermPeriod(SerializableModel):
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    term = models.ForeignKey(Term)
    year = models.IntegerField()

    def normalize(self):
        return {
            'id': self.pk,
            'start_date': self.start_date.strftime("%Y/%m/%d") if self.start_date else None,
            'end_date': self.end_date.strftime("%Y/%m/%d") if self.end_date else None,
            'term': self.term.normalize(),
            'year': self.year
        }


class Class(SerializableModel):
    WEEKDAYS = ((None, None),) + tuple(
        (day, day) for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    )

    subject = models.ForeignKey(Subject, related_name='classes')
    day_of_week = models.CharField(max_length=3, choices=WEEKDAYS, null=True)
    start_period = models.ForeignKey(Period, null=True, related_name="start_period")
    end_period = models.ForeignKey(Period, null=True, related_name="end_period")
    classroom = models.ForeignKey(Classroom, null=True)
    term = models.ForeignKey(Term, null=True)

    def normalize(self):
        return {
            'id': self.pk,
            'day_of_week': self.day_of_week,
            'term': self.term.normalize(),
            'start_period': self.start_period.normalize() if self.start_period else None,
            'end_period': self.end_period.normalize() if self.end_period else None,
            'classroom': self.classroom.normalize() if self.classroom else None,
            'subject': self.subject.pk
        }
