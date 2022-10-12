from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('post/list/', views.post_list, name='post_list'),
    path('post/<int:pk>/detail/', views.post_detail, name='post_detail'),
    path('new/post/', views.new_post, name='new_post'),
    path('edit/<int:pk>/post/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comment/<int:pk>/delete/', views.PostCommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/edited/', views.PostCommentUpdate.as_view(), name='comment_edit'),
]
