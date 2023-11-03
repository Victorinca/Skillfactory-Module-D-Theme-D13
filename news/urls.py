from django.urls import path, include
# импортируем наше представление
from .views import PostsList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearchView, PostCategoryView
#from .views import CommentCreateView#, CommentUpdateView
from .views import SubscribeView, UnsubscribeView, respond_to_post, accept_comment, delete_comment
#, subscribe_to_category, unsubscribe_from_category
from .views import HomePageView

app_name = 'news'
urlpatterns = [
#   path('', MainView.as_view(), name='index'),
# path -- означает путь. В данном случае путь ко всем постам у нас останется пустым, позже станет ясно почему
    # т.к. PostsList сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('', HomePageView, name='home'), # главная
    path('news/', PostsList.as_view(), name='newslist'), # name='posts' или 'news'
    # pk -- это первичный ключ объекта, который будет выводиться у нас в шаблон
    path('news/<int:pk>/', PostDetailView.as_view(), name='post_detail'), # +Ссылка на детали объекта (поста)
    path('add/', PostCreateView.as_view(), name='post_create'), # +Ссылка на создание объекта (поста)
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_create'), # Ссылка на редактирование объекта (поста)
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # +Ссылка на удаление объекта (поста)
    path('news/search/', PostSearchView.as_view(), name='post_search'), # Ссылка на страницу поиска объектов (постов)
    path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('unsubscribe/<int:pk>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('news/<int:post_id>/comment/', respond_to_post, name='post_comment'), # Ссылка на создание объекта (поста)
    path('news/accept_comment/<int:comment_id>/', accept_comment, name='accept_comment'),
    path('news/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]