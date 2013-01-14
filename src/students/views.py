from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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

    if 'login_redirect' in request.session:
        return HttpResponseRedirect(request.session['login_redirect'])
    else:
        return HttpResponseRedirect(reverse('index'))
