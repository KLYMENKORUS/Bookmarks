from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class PublishManager(models.Manager):
    """Добавление своего менеджера"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('published', 'PUBLISHED'),
    )
    title = models.CharField(max_length=250, verbose_name='Post title', help_text='Allowed number of characters 250')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts_created')
    body = models.TextField(verbose_name='Your entry:')
    image = models.ImageField(upload_to='posts', blank=True, verbose_name='Photo recording')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    users_like = models.ManyToManyField(User, related_name='posts_likes', blank=True)

    object = models.Manager() # Менеджер по умолчанию.
    published = PublishManager() # Новый менеджер.
    tags = TaggableManager()

    def get_absolute_url(self):
        """Канонические URL’ы для моделей"""
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Your nickname:', null=True, blank=True)
    body = models.TextField(help_text="Enter your comment", verbose_name='Your comment:')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
