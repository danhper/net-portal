from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import render
from courses.models import Period
from extended_models.models import SerializableList

def index(request):
    registrations = request.user.get_profile().get_subjects()
    periods = SerializableList(Period.objects.all())
    return render(request, "course_navi/index.html", {
            'user': request.user,
            'registrations': registrations,
            'periods': periods,
            'unread_messages': 20
        })

def timetable(request):
    t = loader.get_template("course_navi/timetable.html")
    return HttpResponse(t.render(Context({})))

def message(request):
    t = loader.get_template("course_navi/message.html")
    return HttpResponse(t.render(Context({})))

def news(request):
    t = loader.get_template("course_navi/news.html")
    return HttpResponse(t.render(Context({})))

def settings(request):
    t = loader.get_template("course_navi/settings.html")
    return HttpResponse(t.render(Context({})))

def lecture(request):
    t = loader.get_template("course_navi/lecture.html")
    return HttpResponse(t.render(Context({})))
