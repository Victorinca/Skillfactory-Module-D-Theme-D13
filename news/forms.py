from django.forms import ModelForm
from .models import Author, Category, Post, PostCategory, Comment, Subscription, SubscriptionCategory
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from tinymce.widgets import TinyMCE


# Создаём модельную форму для создания, редактирования объектов (постов)
class PostForm(ModelForm):
    postCats = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите категории поста'
    )
    postAuthor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select,
        label='Выберите автора'
    )

# В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля.
# Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Post
        fields = ['post_type', 'postTitle', 'postText', 'postCats', 'postAuthor']
        widgets = {
            'post_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'postTitle' : forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заголовок поста',
            }),
            'postText' : forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текст поста',
            }),
        }
        labels = {
            'post_type': 'Выберите тип поста',
            'postTitle': 'Заголовок',
            'postText': 'Текст',
        }


class BasicSignupForm(SignupForm):

     def save(self, request):
         user = super(BasicSignupForm, self).save(request)
         common_group = Group.objects.get_or_create(name='common')[0]
         common_group.user_set.add(user)
         return user


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        #fields = ('commentText',)
        fields = ['commentText']
        widgets = {
            'commentText' : forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текст',
            }),
        }
        labels = {
            'commentText': 'Текст отклика',
        }
