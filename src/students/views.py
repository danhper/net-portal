from django.template import loader, Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import django.contrib.auth as auth
from api import NetPortalAPI


def login(request):
  t = loader.get_template("students/login.html")
  return HttpResponse(t.render(Context({})))


def make_login(request):
    if request.method != 'POST':
        return login(request)

    username, password = (request.POSt.get(s) for s in ["username", "password"])

    try:
        # manually fetch user to create account on first log in
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        api = NetPortalAPI()
        if api.login(username, password):
            api.login_cnavi()
            User.students.create_with_subjects(username, password, api.get_subjects())

    user = auth.authenticate(username, password)

    if user is None:
        messages.error(request, _("login.error"))
        return login(request)

    auth.login(request, user)

    if 'login_redirect' in request.session:
        return HttpResponseRedirect(request.session['login_redirect'])
    else:
        return HttpResponseRedirect(reverse('index'))
