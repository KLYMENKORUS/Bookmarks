from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth
from . import views


#app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('registration/done/', views.register_done, name='register_done'),
    path('profile/', views.profile, name='profile'),
    # Шаблоны для доступа к обработчикам смены пароля.
    path('password_change/', auth.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Обработчики восстановления пароля.
    path('password_reset/', auth.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Обработчики подписок
    path('users/', views.user_list, name='users_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    # обрабочик удаления пользователя
    path('profile/delete/', views.UserDeleteView.as_view(), name='user_delete'),

]
