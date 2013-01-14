from django import forms
from django.forms import fields
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from api import NetPortalAPI
import django.contrib.auth as auth
from django.utils.translation import ugettext as _


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
            api = NetPortalAPI()
            if api.login(username, password):
                api.login_cnavi()
                subjects = api.get_subjects()
                User.students.create_with_subjects(username, password, subjects)

        user = auth.authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError(_("login.error"))
        else:
            cleaned_data["user"] = user

        return cleaned_data
