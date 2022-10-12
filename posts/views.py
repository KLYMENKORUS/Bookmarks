from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import DeleteView, UpdateView
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from actions.utils import create_action
from actions.models import Action
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    # По умолчанию, отображаем все действия
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # Если текущий пользователь подписался на кого то,
        # отображаем только действия этих пользователей
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    try:
        action = paginator.page(page)
    except PageNotAnInteger:
        action = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        action = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'actions/detail.html', {'action': action})
    context = {'action': action,
               'page': page,
               'actions': actions}
    return render(request, 'posts/list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Список активных коментариев для этой статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий но не сохраняем в БД
            new_comment = comment_form.save(commit=False)
            # Привязка статьи, автора
            new_comment.user = request.user
            new_comment.post = post
            # Сохраняем в БД
            new_comment.save()
            create_action(request.user, 'commented on the post', post)
            messages.success(request, 'Comment added successfully')
    else:
        comment_form = CommentForm()
    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'posts/detail.html', context)


@login_required()
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            create_action(request.user, 'added a post', post)
            messages.success(request, 'Write successfully added')
            return redirect('posts:post_detail', pk=post.pk)
    context = {'form': form}
    return render(request, 'posts/new_post.html', context)


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        edit_form = PostForm(request.POST, instance=post, files=request.FILES)
        if edit_form.is_valid():
            post = edit_form.save(commit=False)
            post.author = request.user
            post.save()
            create_action(request.user, 'edited entry', post)
            messages.success(request, 'Entry successfully edited')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        edit_form = PostForm(instance=post)
    context = {'edit_form': edit_form}
    return render(request, 'posts/edit_post.html', context)


class PostDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_message = 'Entry successfully deleted'

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'username': self.object.author})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCommentUpdate(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    success_message = 'Your comment successfully edited'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post_id})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


class PostCommentDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    success_message = 'Your comment successfully deleted'

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post_id})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

