# import django_filters
# импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter, ChoiceFilter, BooleanFilter
from django import forms
from django.shortcuts import render
from .models import Post, Author, Category, PostCategory, Comment
from django.contrib.auth.models import Group, User

# создаём фильтр для поиска объектов (постов)
class PostFilter(FilterSet):
    #postCreated = forms.DateField(field_name='postCreated', lookup_expr='date__gt', input_formats=['%d-%m-%Y'])
    postCreated = DateFilter(
        field_name='postCreated',
        lookup_expr='date__gt',
        label='Дата создания позже, чем',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'дд.мм.гггг'
            }
        )
    )

    post_type = ChoiceFilter(
        field_name='post_type',
        choices=Post.POST_TYPE,
        lookup_expr='exact',
        label='Тип',
    )

    postTitle = CharFilter(
        field_name='postTitle',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )

    postAuthor = ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='postAuthor',
        lookup_expr='exact',
        label='Никнейм автора',

    )

    # Здесь в мета классе надо предоставить модель и указать поля,
# по которым будет фильтроваться (т.е. подбираться) информация о постах
    class Meta:
        model = Post
# поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = ('postCreated', 'post_type', 'postTitle', 'postAuthor')

        # fields = ['postAuthor', 'post_type']
        #
        # def filter_by_author_and_type(self, queryset, name, value):
        #     return queryset.filter(postAuthor=value[0], post_type=value[1])

# способ 1
#        fields = ('post_type', 'postCats', 'postRating', 'postAuthor', 'postCreated', 'postTitle', 'postText')
# способ 2
#        fields = {
#            'post_type': ['exact'], # Поле для работы с choices
#            'postCats': ['exact'], # Поле для работы с choices
#            'postRating': ['gt']  # больше, чем указал пользователь
#            'postAuthor': ['exact'], # Поле для работы с choices
#            'postCreated': ['date__gt'], # больше указаной даты
# Мы хотим, чтобы нам выводился заголовок, хотя бы отдалённо похожий на то, что запросил пользователь
#            'postTitle': ['icontains'],
#            'postText': ['icontains'], # Ищем по ключевым словам в тексте
#        }



class CommentFilter(FilterSet):
    commentForPost__postTitle = CharFilter(lookup_expr='icontains', label='Заголовок объявления')
    commentText = CharFilter(lookup_expr='icontains', label='Текст отклика')
    comment_is_accepted = BooleanFilter(field_name='comment_is_accepted', label='Отклик принят?')

    class Meta:
        model = Comment
        fields = ['commentForPost__postTitle', 'commentText', 'comment_is_accepted']
        # fields = ('commentForPost', 'commentText', 'comment_is_accepted')

    def __init__(self, *args, **kwargs):
        super(CommentFilter, self).__init__(*args, **kwargs)
        self.form.fields['commentForPost__postTitle'].widget.attrs.update(
            {'placeholder': 'Поиск по названию объявления'})
        self.form.fields['commentText'].widget.attrs.update({'placeholder': 'Поиск по тексту отклика'})

