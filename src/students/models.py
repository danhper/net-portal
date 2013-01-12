from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
import base64
import rsa

class StudentProfile(models.Model):
    """Class to use as user profile"""
    user = models.OneToOneField(User)
    encrypted_password = models.CharField(max_length=200)

@receiver(pre_save, sender=User)
def save_email(sender, user, **kwargs):
    if not user.username or not user.password:
        raise ValueError("A user needs a username and a password")

    if user.password.startswith("pbkdf2_sha256") and user.password.endswith("="):
        raise ValueError("Need unhashed password to create user.")

    if not user.email:
        user.email = user.username

    with open(settings.RSA["public_key_path"], "r") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypted_password = rsa.encrypt(user.password, public_key)
    b64_encrypted_password = base64.b64encode(encrypted_password)

    # temporary field for encrypted password
    user.encrypted_password = b64_encrypted_password

    # insert hashed password in database
    user.password = make_password(user.password)


@receiver(post_save, sender=User)
def create_profile(sender, user, created, **kwargs):
    profile, new = StudentProfile.objects.get_or_create(user=user, encrypted_password=user.encrypted_password)
    user.encrypted_password = None
