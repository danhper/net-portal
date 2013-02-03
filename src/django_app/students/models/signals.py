from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from models import StudentProfile

@receiver(pre_save, sender=User)
def prepare_user_creation(sender, instance, **kwargs):
    # only run on creation, not on update
    if instance.pk is not None:
        return

    if not instance.username or not instance.password:
        raise ValueError("A instance needs a username and a password")

    # check if password is hashed. need to adapt for other hash
    if instance.password.startswith("pbkdf2_sha256") and instance.password.endswith("="):
        # need to check if called from CLI
        pass
        # raise ValueError("Need unhashed password to create instance. Current: {0}.".format(instance.password))
    else:
        profile = StudentProfile()
        profile.set_password(instance.password)

        # bind temporary profile while no pk
        instance.profile = profile
        # insert hashed password in database
        instance.password = make_password(instance.password)

    if not instance.email:
        instance.email = instance.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # only run on creation, not on update
    if not created:
        return

    if hasattr(instance, 'profile'):
        instance.profile.user = instance
        instance.profile.save()
        instance.profile = None
