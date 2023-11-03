from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscription#, SubscriptionCategory

# Register your models here.
admin.site.register(Author)
#admin.site.register(Category)
#admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
#admin.site.register(Subscription)
#admin.site.register(SubscriptionCategory)


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 0
class PostAdmin(admin.ModelAdmin):
    list_display = ('postCreated', 'post_type', 'postTitle', 'postRating', 'postAuthor')
    inlines = [PostCategoryInline]
    #filter_horizontal = ('postCats',)

admin.site.register(Post, PostAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriptionUser', 'get_subscribed_categories') # Отображение полей в таблице
    list_filter = ('subscriptionCategories',) # Фильтрация по категориям
    search_fields = ('subscriptionUser__username',) # Поиск по имени пользователя

    def get_subscribed_categories(self, obj):
        return ", ".join([category.categoryName for category in obj.subscriptionCategories.all()])
    get_subscribed_categories.short_description = 'Subscribed Categories' # Заголовок столбца

admin.site.register(Subscription, SubscriptionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'get_subscribers')  # Определяет, какие поля отображать в таблице
    search_fields = ('categoryName',)  # Определяет, по каким полям можно выполнять поиск

    def get_subscribers(self, obj):
        return ", ".join([user.username for user in obj.subscribers.all()])  # Возвращает список подписчиков в виде строки
    get_subscribers.short_description = 'Подписчики'  # Определяет заголовок столбца в таблице

admin.site.register(Category, CategoryAdmin)
