from django import forms
from django.forms import fields
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth as auth
from django.utils.translation import ugettext as _

from api import NetPortalException
from courses.models import Subject

class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=fields.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            return cleaned_data

        try:
            # manually fetch user to create account on first log in
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            try:
                (subjects, user_info) = Subject.get_from_api(username, password, 'all', True)
                User.students.create_with_info(username, password, user_info, subjects)
            except NetPortalException:
                pass

        user = auth.authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError(_("login.error"))
        else:
            cleaned_data["user"] = user

        return cleaned_data
