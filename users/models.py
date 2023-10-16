from django.conf import settings
from django.db import models
from PIL import Image

from django.db.models.signals import post_save
from django.dispatch import receiver

user = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    """Stores the user profile"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    image = models.ImageField(
        default='static/profile_pics/default.jpeg', upload_to='profile_pics')

    def __str__(self) -> str:
        return self.user.username

    # resize the image while saving
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# create a profile for each user creates
@receiver(post_save, sender=user)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=user)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()
