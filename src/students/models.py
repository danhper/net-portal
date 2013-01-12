from django.db import models
from django.contrib.auth.models import User

class StudentProfile(object):
    """Class to use as user profile"""
    user = models.OneToOneField(User)
    encrypted_password = models.CharField(max_length=200)
