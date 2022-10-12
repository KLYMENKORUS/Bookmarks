from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    #path('list/', views.ImageListView.as_view(), name='image_list'),
    path('list/', views.image_list, name='image_list'),
    path('create/images/', views.image_create, name='create'),
    path('detail/<int:pk>/images/', views.image_detail, name='detail'),
    path('<int:pk>/edit/', views.image_edit, name='image_edit'),
    path('delete/<int:pk>/', views.ImagesDeleteView.as_view(), name='Image_delete'),
    path('delete/comment/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('edited/comment/<int:pk>/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('like/', views.image_like, name='like'),

]
