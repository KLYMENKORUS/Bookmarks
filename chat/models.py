from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class ChatManager(models.Manager):
    use_for_related_fields = True

    def unread(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_read=False)
        return qs.exclude(last_message__author=user) if user else qs


class Chat(models.Model):
    """Model Chat"""
    DIALOG = 'D'
    Chat = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (Chat, _('Chat'))
    )

    type = models.CharField(_('Type'), max_length=1, choices=CHAT_TYPE_CHOICES, default=DIALOG)
    members = models.ManyToManyField(User, verbose_name='Participant')
    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True,
                                     on_delete=models.SET_NULL)

    object = ChatManager()

    def get_absolute_url(self):
        return reverse_lazy('chat:message', kwargs={'chat_id': self.pk})


class Message(models.Model):
    """Model Message"""
    chat = models.ForeignKey(Chat, verbose_name=_('Chat'), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    message = models.TextField(_('Message'))
    pub_date = models.DateTimeField(_('Message date'), default=timezone.now)
    is_read = models.BooleanField(_('Read'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message

