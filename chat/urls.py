from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path('dialog/create/<int:user_id>/', views.CreateDialogView.as_view(), name='create_dialog'),
    path('dialogs/<int:chat_id>/', views.MessagesView.as_view(), name='message'),
    path('delete/<int:pk>/', views.ChatDeleteView.as_view(), name='chat_delete'),
]
