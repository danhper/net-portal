from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

def index(request):
    return HttpResponseRedirect(reverse('cnavi:index'))

def about(request):
    return render(request, "net_portal/about.html")

def team(request):
    return render(request, "net_portal/team.html")

def contact(request):
    return render(request, "net_portal/contact.html")