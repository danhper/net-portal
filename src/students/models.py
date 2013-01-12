from django.db import models

class StudentProfile(object):
    """Class to use as user profile"""
    user = models.OneToOneField(models.User)
    encrypted_password = models.CharField(max_length=200)
