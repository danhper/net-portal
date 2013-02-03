from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

import models as m

class RegistrationManager(models.Manager):
    def get_with_related(self, **kwargs):
        # Ugly fix to reduce database hits...
        cr = ['classes', 'classes__term', 'classes__start_period']
        cr += ['classes__end_period', 'classes__classroom']
        cr += ['classes__classroom__building', 'classes__subject']
        tr = ['teachers', 'teachers__school']
        subject_related = ['subject__{0}'.format(v) for v in cr + tr]
        return m.SubjectRegistration.objects.select_related().prefetch_related(*subject_related).filter(**kwargs)

    def reorder(self, old_order, new_order):
        if old_order == new_order:
            return
        if old_order < new_order:
            m.SubjectRegistration.objects.filter(order__gt=old_order, order__lte=new_order).update(order=F('order') - 1)
        else:
            m.SubjectRegistration.objects.filter(order__gte=new_order, order__lt=old_order).update(order=F('order') + 1)


class StudentManager(models.Manager):
    def create_with_info(self, username, password, info, subjects):
        p = User.objects.create(username=username, password=password).get_profile()
        p.__dict__.update(**info)
        p.add_subjects(subjects)
        p.save()

StudentManager().contribute_to_class(User, 'students')
