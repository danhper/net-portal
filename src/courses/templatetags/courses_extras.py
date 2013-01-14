from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def class_time(class_obj):
    if class_obj.day_of_week:
        dow = class_obj.get_day_of_week_display()
    else:
        dow = _("none")

    if class_obj.start_period is None or class_obj.end_period is None:
        return dow

    start = class_obj.start_period.pk
    end = class_obj.end_period.pk
    if start == end:
        return dow + _('period %(period)d') % {'period': start}
    else:
        p = _('from period %(start)d to %(end)d') % {'start': start, 'end': end}
        return dow + p
