from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from .models import Profile
from django.views import View
from django.contrib.auth.models import User
from images.models import Image
from django.http import JsonResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from .models import Contact
from actions.utils import create_action
from actions.models import Action
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here.
def dashboard(request):
    return render(request, 'registration/dashboard.html')


def register_done(request):
    return render(request, 'registration/register_done.html')


class RegistrationView(View):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'registration/registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='register_done')

        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            create_action(new_user, 'has created an account')
            messages.success(request, f'{new_user} was created successfully')
            return HttpResponseRedirect(reverse('register_done'))
        else:
            messages.error(request, 'Error filling out the registration form!')
        return render(request, self.template_name, {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated your successfully!')
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, 'Error updating your profile!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {'user_form': user_form,
               'profile_form': profile_form}
    return render(request, 'account/profile.html', context)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account/user_delete.html'
    success_url = reverse_lazy('dashboard')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted successfully!')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


@login_required()
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'users': users})


@login_required()
def user_detail(request, username, count=4):
    user = get_object_or_404(User, username=username, is_active=True)
    follows = User.objects.filter(rel_form_set__user_to=True)
    img = Image.object.filter(user=user)[:count]
    return render(request, 'account/user/detail.html', {'user': user,
                                                        'img': img,
                                                        'follows': follows})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_form=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_form=request.user, user_to=user).delete()
                create_action(request.user, 'is unsubscribed', user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


