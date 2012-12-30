from django.template import loader, Context
from django.http import HttpResponse

def login(request):
  t = loader.get_template("students/login.html")
  return HttpResponse(t.render(Context({})))
