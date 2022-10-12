from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class PublishManager(models.Manager):
    """Добавление своего менеджера"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Image(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('published', 'PUBLISHED'),
    )
    user = models.ForeignKey(User, related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images', blank=True, verbose_name='Your images:')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(User, related_name='images_likes',
                                        blank=True)

    object = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', kwargs={'pk': self.pk})

    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Your nickname:', null=True, blank=True,
                               related_name='author_comments')
    body = models.TextField(help_text="Enter your comment", verbose_name="Your comment:", max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.author} on {self.image}'

