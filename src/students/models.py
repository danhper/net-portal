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

    @property
    def plain_password(self):
        with open(settings.RSA["private_key_path"], "r") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        encrypted_password = base64.b64decode(self.encrypted_password)
        return rsa.decrypt(encrypted_password, private_key)


@receiver(pre_save, sender=User)
def prepare_user_save(sender, instance, **kwargs):
    if not instance.username or not instance.password:
        raise ValueError("A instance needs a username and a password")

    if instance.password.startswith("pbkdf2_sha256") and instance.password.endswith("="):
        raise ValueError("Need unhashed password to create instance.")

    if not instance.email:
        instance.email = instance.username

    with open(settings.RSA["public_key_path"], "r") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypted_password = rsa.encrypt(instance.password, public_key)
    b64_encrypted_password = base64.b64encode(encrypted_password)

    # temporary field for encrypted password
    instance.encrypted_password = b64_encrypted_password

    # insert hashed password in database
    instance.password = make_password(instance.password)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    profile, new = StudentProfile.objects.get_or_create(user=instance, encrypted_password=instance.encrypted_password)
    instance.encrypted_password = None
