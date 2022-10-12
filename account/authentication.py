from django.contrib.auth.models import User
from django.contrib import messages


class EmailAuthBackend(object):
    """Выполняет аутентификацию пользователя по e-mail."""

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return messages.error(request, 'Invalid password')
        except User.DoesNotExist:
            return messages.error(request, 'User is not found')

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None