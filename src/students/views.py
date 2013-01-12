from django.template import loader, Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

def login(request):
  t = loader.get_template("students/login.html")
  return HttpResponse(t.render(Context({})))


def make_login(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('login'))
    username = request.POST.get("username")
    password = request.POST.get("password")

    try:
        # manually fetch user to create account on first log in
        user = User.objects.get(username=username)

        if not check_password(password, user.password):
            messages.error(request, _("login.error"))
            return login(request)
    except ObjectDoesNotExist:
        create_user()

    if 'login_redirect' in request.session:
        return HttpResponseRedirect(request.session['login_redirect'])
    else:
        return HttpResponseRedirect(reverse('index'))

    t = loader.get_template("students/login.html")
    return HttpResponse(t.render(Context({})))

def create_user(username, password):
    user = User.create(username=username, password=password)

