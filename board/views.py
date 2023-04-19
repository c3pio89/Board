from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView,\
    DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from .filters import CommentFilter
from .models import Category, Comment, Author, NewsLetter, Code
from .forms import NewsForm, CommentForm, NewsLetterForm, ConfirmationCodeForm

class CategoryList(ListView):
    model = Category
    ordering = '-time'
    template_name = 'news_all.html'
    context_object_name = 'news'
    paginate_by = 10


class CategoryListSearch(ListView):
    model = Category
    ordering = '-time'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 4


class CategoryDetail(DetailView):
    model = Category
    template_name = 'news_id.html'
    context_object_name = 'news_id'


class CommentDetail(DetailView):
    model = Comment
    template_name = 'comments_id.html'
    context_object_name = 'comments_id'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = NewsForm
    model = Category
    template_name = 'news_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(f'user = {self.request.user} name = {self.request.user.username}')

        obj, created = Author.objects.get_or_create(
            authorUser=self.request.user
        )
        print(f'author = {self.request.user.author} obj = {obj}')
        self.object.author = obj
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    raise_exception = True
    form_class = NewsForm
    model = Category
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.id = self.kwargs['pk']
        print(f'post.id = {post.id}')
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    raise_exception = True
    model = Category
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    context_object_name = 'news_id'


class CommentCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_comment')
    raise_exception = True
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        # переопределение метода, чтобы добавить commentUser - текущего пользователя

        # print(f'user = {self.request.user} name = {self.request.user.username}')
        comment = form.save(commit=False)
        comment.commentUser = self.request.user
        post_id = self.kwargs['pk']
        comment.commentPost = get_object_or_404(Category, id=post_id)
        return super().form_valid(form)


class CommentSearch(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_comment', 'news.add_post')
    raise_exception = True
    model = Comment
    ordering = '-dateCreation'
    template_name = 'comment_search.html'
    context_object_name = 'comment_search'
    paginate_by = 4
    def get_queryset(self):
        queryset = super().get_queryset()

        user_current = self.request.user

        post_by_current_user = Category.objects.filter(author=user_current.author)

        queryset = queryset.filter(commentPost__in=post_by_current_user)

        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@permission_required('news.delete_comment')
def comment_accept(request, pk):
    """Accept comment to author's post"""
    comment_accepted = Comment.objects.get(id=pk)
    comment_accepted.status = True
    comment_accepted.save()
    message = 'Вы успешно приняли отклик на свое объявление'
    return render(request, 'comment_action_confirm.html', {'comment': comment_accepted, 'message': message})


@permission_required('news.delete_comment')
def comment_delete(request, pk):
    """Delete comment to author's post"""
    comment_to_delete = Comment.objects.get(id=pk)
    comment_to_delete.delete()
    message = 'Вы успешно удалили отклик на свое объявление'
    return render(request, 'comment_action_confirm.html', {'comment': comment_to_delete, 'message': message})


class CommentList(PermissionRequiredMixin, ListView):
    """Lists all accepted comments to a specific post. Page can be reached while reviewing a post."""

    permission_required = ('news.view_comment', 'news.view_post')
    raise_exception = True
    model = Comment
    ordering = '-dateCreation'
    context_object_name = 'comment_list'
    template_name = 'comment_list.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs['pk']
        queryset = queryset.filter(commentPost_id=post_id)
        queryset = queryset.filter(status=True)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id_ = self.kwargs['pk']
        postCommented = Category.objects.get(id=post_id_).text

        context['post_id'] = post_id_
        context['post_commented'] = postCommented

        return context


class NewsLetterCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_newsletter')
    raise_exception = True
    form_class = NewsLetterForm
    model = NewsLetter
    template_name = 'newsletter_create.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        # переопределение метода, чтобы добавить пользователя
        newsletter = form.save(commit=False)
        newsletter.userNewsletter = self.request.user
        return super().form_valid(form)


class ConfirmationCode(PermissionRequiredMixin, UpdateView):
    # class ConfirmationCode(UpdateView):
    model = Code
    permission_required = ('news.change_post')
    raise_exception = True
    template_name = 'user_confirm_code.html'
    form_class = ConfirmationCodeForm
    success_url = '/news'

    def form_valid(self, form):
        # переопределение метода, чтобы добавить user - текущего пользователя
        code = form.save(commit=False)
        code.user = self.request.user
        return super().form_valid(form)

class HomePageView(ListView):
    model = Category
    template_name = 'home_page.html'