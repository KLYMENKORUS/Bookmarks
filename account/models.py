from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True, help_text='YYYY-MM-DD')
    profile_photo = models.ImageField(upload_to='users', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @property
    def get_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        else:
            return '/static/images/default.jpg'


class Contact(models.Model):
    user_form = models.ForeignKey('auth.User', related_name='rel_form_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_form} follows {self.user_to}'


# Динамическое добавление поля following в модель User
User.add_to_class('following', models.ManyToManyField('self',
                                                      through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))

