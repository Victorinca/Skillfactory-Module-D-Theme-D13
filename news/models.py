# импорт скрипта models из модуля django.db
from django.db import models
from django.utils import timezone
from datetime import datetime
# импорт скрипта пользователя
from django.contrib.auth.models import User
# импорт функции Sum,
# предоставляющей возможность выполнять агрегацию суммы значений поля в запросах к базе данных
from django.db.models import Sum
# для удаления всех HTML-тегов из строки
from django.utils.html import strip_tags
# для обратного поиска URL-адреса на основе имени шаблона URL или объекта представления,
# когда нужно сгенерировать URL-адрес в коде, а не в шаблоне.
from django.urls import reverse
#from audioop import reverse
#
from tinymce.models import HTMLField

# Create your models here.
# наследуемся от класса Model, определяющего основные функции работы с моделью
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser.username}'

    # def __str__(self):
    #     return f'{self.id}) НИКНЕЙМ АВТОРА: {self.authorUser.username}; \n' \
    #            f'ФАМИЛИЯ: {self.authorUser.last_name};  ИМЯ: {self.authorUser.first_name}; \n' \
    #            f'ЭЛ ПОЧТА: {self.authorUser.email}'

# Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
    def update_rating(self):
# 1) суммарный рейтинг каждой статьи postRating автора postAuthor умножается на 3
        sumPR = self.post_set.all().aggregate(sumPostRating=Sum('postRating'))
        # с помощью post_set.all() - получим все связанные с автором посты в модели Post,
        # и с помощью aggregate получаем все значения поля рейтинг и суммируем их
        # далее создадим промежуточную переменную
        pRate = 0
        pRate += sumPR.get('sumPostRating')
# 2) суммарный рейтинг всех комментариев commentRating автора authorUser
        sumAuthorCR = self.authorUser.comment_set.all().aggregate(sumAuthorComRating=Sum('commentRating'))
        authorCRate = 0
        authorCRate += sumAuthorCR.get('sumAuthorComRating')
# 3) суммарный рейтинг всех комментариев commentRating к статьям автора postAuthor
        sumPostCR = Comment.objects.filter(commentForPost__postAuthor=self).values('commentRating').aggregate(sumPostComRating=Sum('commentRating'))
        postCRate = 0
        postCRate += sumPostCR.get('sumPostComRating')

# print('pRate =', pRate * 3, 'authorCRate =', authorCRate, 'postCRate =', postCRate)
        self.authorRating = pRate * 3 + authorCRate + postCRate
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True) # подписчики related_name='subscribed_categories'
    #is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.categoryName}'

    # def __str__(self):
    #     users = self.subscribers.all()
    #     users_names = [f"{User.id}) {User.username}" for User in users]
    #     #subscribers_names = ', '.join([User.username for User in self.subscribers.all()])
    #     return f'{self.id}) НАИМЕНОВАНИЕ КАТЕГОРИИ: {self.categoryName}; \n' \
    #            f'ПОДПИСЧИКИ: {", ".join(users_names)}'
    #            #f'ПОДПИСЧИКИ: {subscribers_names}'

    def get_absolute_cat_url(self):
        return reverse('news:category', args=[str(self.id)])


class Post(models.Model):
    selling = 'S'
    buying = 'B'

    POST_TYPE = [
        (selling, "Продам"),
        (buying, "Куплю")
    ]

    postAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POST_TYPE, default=selling)
    #postType = models.CharField(max_length=1, choices=POSTTYPE, default=selling)
    postCreated = models.DateTimeField(auto_now_add=True)
    postCats = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=128, db_index=True)
    postText = models.TextField()
    #postText = HTMLField()
    postRating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'Пост № {self.id} - Заголовок: {self.postTitle}'

    #def __str__(self):
    #    return self.postTitle

# Установка лимита на публикации: один пользователь не может публиковать более трёх новостей в сутки
    def save(self, *args, **kwargs):
        # Проверяем, сколько постов уже опубликовал пользователь в течение суток
        posts_count = Post.objects.filter(postAuthor=self.postAuthor,
                                          postCreated__gte=timezone.now() - timezone.timedelta(days=1)).count()
        if posts_count >= 3:
        # Если количество постов больше или равно 3, вызываем исключение
            raise Exception("Вы уже опубликовали максимальное количество постов за сутки")
        # Если количество постов меньше трех, сохраняем пост
        super().save(*args, **kwargs)

    # def __str__(self):
    #     categories = self.postCats.all()
    #     categories_names = [f"{category.id}) {category.categoryName}" for category in categories]
    #     # category_names = ', '.join([category.categoryName for category in self.postCats.all()])
    #     return f'{self.id}) ДАТА: {self.postCreated.strftime("%d.%m.%Y")}; ТИП: {self.post_type}; РЕЙТИНГ: {self.postRating}; \n' \
    #            f'НИКНЕЙМ АВТОРА: {self.postAuthor.authorUser.username}; \n' \
    #            f'ТЕМА ПОСТА: {self.postTitle}; \n' \
    #            f'КАТЕГОРИИ ПОСТА: {", ".join(categories_names)}'
    #            #f'КАТЕГОРИИ ПОСТА: {category_names}'

    def get_post_type(self):
        return self.get_post_type_display()

    def get_absolute_url(self):
        # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с постом
        # return f'/news/{self.id}'
        # Функция reverse() принимает имя шаблона или объект представления в качестве аргумента
        # и возвращает соответствующий URL-адрес.
        # Если URL-шаблон принимает аргументы, можно передать их в reverse() в виде списка args или словаря kwargs.
        return reverse('news:post_detail', args=[str(self.id)])

# Рейтинг для postRating:
    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

# Метод preview() модели Post, который возвращает
# начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
# вариант 1
#    def preview(self):
#        preview_length = 124
#        return self.postText[:preview_length] + '...' if len(self.postText) > preview_length else self.postText
# вариант 2
    def preview(self):
        return f"{self.postText[:124]}..."
# Модифицированный вариант 2 с функцией strip_tags из модуля django.utils.html.
# Применяем функцию strip_tags к self.postText, чтобы удалить все HTML-теги из текста
#     def preview(self):
#             text_without_tags = strip_tags(self.postText)[:124]
#             return f"{text_without_tags}..."


class PostCategory(models.Model):
    fromPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    fromCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
            return f'{self.id}) КАТЕГОРИЯ № {self.fromCategory}; \n' \
                   f'ПОСТ № {self.fromPost}'


class Comment(models.Model):
    commentForPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentCreated = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)
    comment_is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('news:comment_create', args=[str(self.id)])

    def __str__(self):
        return f"Отклик на объявление '{self.commentForPost.postTitle}' от {self.commentUser.username}"

    # def __str__(self):
    #     return f'{self.id}) ДАТА: {self.commentCreated.strftime("%d.%m.%Y")}; ' \
    #            f'К ПОСТУ № {self.commentForPost.id}; РЕЙТИНГ КОММЕНТАРИЯ: {self.commentRating};\n' \
    #            f'НИКНЕЙМ КОММЕНТАТОРА: {self.commentUser.username}; \n' \
    #            f'ТЕМА ПОСТА: {self.commentForPost.postTitle}; \n' \
    #            f'ТЕКСТ КОММЕНТАРИЯ: {self.commentText}'

# Рейтинг для commentRating:
    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()

# КАК МОЖНО ДОБРАТЬСЯ ЧЕРЕЗ ДЛИННЫЕ СВЯЗИ (НЕСКОЛЬКО СВЯЗЕЙ) ДО КАКОГО-ЛИБО ПОЛЯ.
# Обращаемся в определенной модели к её связанному полю, которое связано с другой моделью,
# у которой есть связанное поле с другой моделью, и так получаем нужное поле.
#     def __str__(self):
#         try:
#             return self.commentForPost.postAuthor.authorUser.username
#         except:
#             return self.commentUser.username


class Subscription(models.Model):
    subscriptionUser = models.ForeignKey(User, on_delete=models.CASCADE)
    #subscriptionUser = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriptionCreated = models.DateTimeField(auto_now_add=True) # Дата подписки
    subscriptionCategories = models.ManyToManyField(Category)  # Категории, на которые подписан user
    #last_notification_sent = models.DateTimeField()  # Дата последней отправки уведомления
    last_notification_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f'Подписка для {self.subscriptionUser.username}'

    # def __str__(self):
    #     cats = self.subscriptionCategories.all()
    #     cats_names = [f"{category.id}) {category.categoryName}" for category in cats]
    #     # cat_names = ', '.join([category.categoryName for category in self.subscriptionCategories.all()])
    #     return f'{self.id}) ДАТА: {self.subscriptionCreated.strftime("%d.%m.%Y")}; \n' \
    #            f'НИКНЕЙМ ПОДПИСЧИКА: {self.subscriptionUser.username}; \n' \
    #            f'КАТЕГОРИИ: {", ".join(cats_names)}'
    #            #f'КАТЕГОРИИ: {category_names}'

class SubscriptionCategory(models.Model):
    fromSubscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    fromCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    # def __str__(self):
    #         return f'{self.id}) КАТЕГОРИЯ № {self.fromCategory}; \n' \
    #                f'ПОДПИСКА № {fromSubscription}'
