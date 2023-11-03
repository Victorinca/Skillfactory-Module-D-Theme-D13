from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Author, Category, Post, PostCategory, Comment, Subscription, SubscriptionCategory
from .views import new_post_subscriptions
from django.contrib.auth.models import User
from django_filters.views import FilterView
from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(post_save, sender=PostCategory)
def notify_subscribers(sender, instance, created, **kwargs):
     if created:
         subject = f'{instance.postTitle}'
     else:
         subject = f'Пост № {instance.id} отредактирован {instance.postTitle}'

     mail_subscribers(
         subject=subject,
         message=instance.message,
     )


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
     if kwargs['action'] == 'post_add':
         new_post_subscriptions(instance)


@receiver(m2m_changed, sender=Category.subscribers.through)
def update_subscription(sender, instance, action, **kwargs):
    if action == 'post_add':
        for user_id in kwargs['pk_set']:
            username = User.objects.get(pk=user_id)  # Получаем экземпляр пользователя
            subscription, created = Subscription.objects.get_or_create(subscriptionUser=username)
            category = Category.objects.get(pk=instance.pk)  # Получаем экземпляр категории
            subscription.subscriptionCategories.add(category)
            subscription_category = SubscriptionCategory.objects.create(fromSubscription=subscription, fromCategory=category)
    elif action == 'post_remove':
        for user_id in kwargs['pk_set']:
            username = User.objects.get(pk=user_id)  # Получаем экземпляр пользователя
            subscription = Subscription.objects.get(subscriptionUser=username)
            category = Category.objects.get(pk=instance.pk)  # Получаем экземпляр категории
            subscription.subscriptionCategories.remove(category)
            SubscriptionCategory.objects.filter(fromSubscription=subscription, fromCategory=category).delete()
    elif action == 'post_remove':
        for user_id in kwargs['pk_set']:
            username = User.objects.get(pk=user_id)  # Получаем экземпляр пользователя
            subscription = Subscription.objects.get(subscriptionUser=username)
            category = Category.objects.get(pk=instance.pk)  # Получаем экземпляр категории
            subscription.subscriptionCategories.change(category)
            SubscriptionCategory.objects.filter(fromSubscription=subscription, fromCategory=category).delete()

# @receiver(m2m_changed, sender=Subscription.subscriptionCategories.through)
# def update_subscriber(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         for user_id in kwargs['pk_set']:
#             username = User.objects.get(pk=user_id)  # Получаем экземпляр пользователя
#             subscription, created = Subscription.objects.get_or_create(subscriptionUser=username)
#             category = Category.objects.get(pk=instance.pk)  # Получаем экземпляр категории
#             category.subscribers.add(subscription)
#             subscriber = Category.objects.create(fromSubscription=subscription, fromCategory=category)
#     elif action == 'post_remove':
#         for user_id in kwargs['pk_set']:
#             username = User.objects.get(pk=user_id)  # Получаем экземпляр пользователя
#             subscription = Subscription.objects.get(subscriptionUser=username)
#             category = Category.objects.get(pk=instance.pk)  # Получаем экземпляр категории
#             category.subscribers.remove(subscription)
#             Category.objects.filter(fromSubscription=subscribers, fromCategory=category).delete()
#     elif action == 'post_remove':
#         for user_id in kwargs['pk_set']:
#             username = User.objects.get(pk=user_id)  # Получаем экземпляр пользователя
#             subscription = Subscription.objects.get(subscriptionUser=username)
#             category = Category.objects.get(pk=instance.pk)  # Получаем экземпляр категории
#             subscription.subscriptionCategories.change(category)
#             Category.objects.filter(fromSubscription=subscribers, fromCategory=category).delete()