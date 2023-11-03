# Не забываем импортировать нужные функции и пакеты
from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
#from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# импортируем необходимые дженерики
from django.views.generic import TemplateView
from django.views import View
from news.models import Category, Post, PostCategory, Comment, Subscription, SubscriptionCategory
from django_filters.views import FilterView
from news.filters import CommentFilter

# Create your views here.
class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        #context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        comments = Comment.objects.filter(commentForPost__postAuthor=user)
        context['comments'] = comments
        comment_filter = CommentFilter(self.request.GET, queryset=comments)
        context['comment_filter'] = comment_filter
        return context

# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе authors
@login_required
def upgrade_me(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
   return redirect('/accounts/cabinet/')

@login_required(login_url='/accounts/login/')
def user_profile(request):
   user_posts = Post.objects.filter(postAuthor=request.user).order_by('-postTitle')
   template = '/accounts/cabinet.html'
   return render(request, template, {'user_posts': user_posts, 'user': request.user})
