from django.template import loader, Context
from django.http import HttpResponse

def index(request):
  t = loader.get_template("course_navi/index.html")
  return HttpResponse(t.render(Context({"unread_messages":20})))

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
