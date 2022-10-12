from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat
from .forms import MessageForm
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class DialogsView(View, LoginRequiredMixin):
    template_name = 'chat/dialog.html'

    def get(self, request,):
        chats = Chat.object.filter(members__in=[request.user.id])
        return render(request, self.template_name, {'user_profile': request.user, 'chats': chats})


class MessagesView(View, LoginRequiredMixin):
    form_class = MessageForm
    template_name = 'chat/messages.html'

    def get(self, request, chat_id):
        unread = Chat.object.unread(user=request.user).count()
        try:
            chat = Chat.object.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
        context = {
            'chat': chat,
            'form': self.form_class,
            'unread': unread
        }
        return render(request, self.template_name, context)

    def post(self, request, chat_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('chat:message', kwargs={'chat_id': chat_id}))


class CreateDialogView(View, LoginRequiredMixin):

    def get(self, request, user_id):
        chats = Chat.object.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.object.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('chat:message', kwargs={'chat_id': chat.id}))


class ChatDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Chat
    template_name = 'chat/chat_delete.html'
    success_url = reverse_lazy('chat:dialogs')
    success_message = 'Chat deleted successfully!'

