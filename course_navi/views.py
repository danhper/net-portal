from django.template import loader, Context
from django.http import HttpResponse

def index(request):
  t = loader.get_template("course_navi/index.html")
  return HttpResponse(t.render(Context({})))
