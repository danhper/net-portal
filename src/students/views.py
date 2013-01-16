from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.http import Http404

import django.contrib.auth as auth
from students.forms import LoginForm


def login(request, form=None):
    if form is None:
        form = LoginForm()
    return render(request, "students/login.html", ({
        'form': form
    }))

def make_login(request):
    if request.method != 'POST':
        return login(request)

    form = LoginForm(request.POST)
    if not form.is_valid():
        return login(request, form)

    user = form.cleaned_data.get("user")

    auth.login(request, user)

    if not form.cleaned_data.get("remember_me"):
        request.session.set_expiry(0)

    if 'login_redirect' in request.session:
        return HttpResponseRedirect(request.session['login_redirect'])
    else:
        return HttpResponseRedirect(reverse('index'))

def logout(request):
    # need to fix link in template to post instead of get
    # if request.method != 'POST':
    #     raise Http404
    auth.logout(request)
    return HttpResponseRedirect(reverse('students:login'))
