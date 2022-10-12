from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import images.views
from .forms import ImageCreateForm, CommentImageForm
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Image, Comment
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from actions.utils import create_action


@login_required()
def image_list(request):
    images = Image.object.filter(user=request.user)
    paginator = Paginator(images, 4)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возращаем первую
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return render(request, 'images/image_list.html', {'images': images})


@login_required()
def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    comments = image.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentImageForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий но не сохраняем в БД
            new_comment = comment_form.save(commit=False)
            # Привязка статьи, автора
            new_comment.author = request.user
            new_comment.image = image
            # Сохраняем в БД
            new_comment.save()
            create_action(request.user, 'commented on the photo', image)
            messages.success(request, 'Comment added successfully')
    else:
        comment_form = CommentImageForm()
    context = {
        'image': image,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form}
    return render(request, 'images/detail.html', context)


@login_required
def image_create(request):
    if request.method == 'POST':
        # Форма отправлена.
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # Данные формы валидны.
            new_item = form.save(commit=False)
            # Добавляем пользователя к созданному объекту.
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'added a photo', new_item)
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect('images:detail', pk=new_item.pk)
    else:
        # Заполняем форму данными из GET-запроса.
        form = ImageCreateForm()
    return render(request, 'images/create.html', {'form': form})


@login_required()
def image_edit(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        edit_form_image = ImageCreateForm(request.POST, instance=image, files=request.FILES)
        if edit_form_image.is_valid():
            picture = edit_form_image.save(commit=False)
            picture.user = request.user
            picture.save()
            create_action(request.user, 'edited details photo', picture)
            messages.success(request, 'Detail successfully edited')
            return redirect('images:detail', pk=picture.pk)
    else:
        edit_form_image = ImageCreateForm(instance=image)
    context = {'edit_form_image': edit_form_image}
    return render(request, 'images/image_edit.html', context)


class ImagesDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Image
    success_url = reverse_lazy('images:image_list')
    success_message = 'Your photo successfully deleted'

    def test_func(self):
        image = self.get_object()
        if self.request.user == image.user:
            return True
        return False


class CommentUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentImageForm
    success_message = 'Your comment successfully edited'

    def get_success_url(self):
        return reverse_lazy('images:detail', kwargs={'pk': self.object.image_id})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class CommentDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    success_message = 'Your comment successfully deleted'

    def get_success_url(self):
        return reverse_lazy('images:detail', kwargs={'pk': self.object.image_id})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


@ajax_required
@login_required()
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.object.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})











