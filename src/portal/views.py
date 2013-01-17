from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

def index(request):
    return HttpResponseRedirect(reverse('cnavi:index'))

def about(request):
    return render(request, "students/about.html")

def team(request):
    return render(request, "students/team.html")

def contact(request):
    return render(request, "students/contact.html")