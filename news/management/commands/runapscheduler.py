import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail
from datetime import datetime, timedelta

from news.models import Subscription, Post


logger = logging.getLogger(__name__)


def my_job():
    # Получить текущую дату
    today = datetime.now()
    # Определить начало предыдущей недели (по вашему определению недели)
    last_week_start = today - timedelta(weeks=1)
    # Найти пользователей с подписками
    subscriptions = Subscription.objects.all()

    for subscription in subscriptions:
        # Определить подписанные категории для пользователя
        categories = subscription.subscriptionCategories.all()
        # Найти новые статьи из подписанных категорий, опубликованные за последнюю неделю
        new_articles = Post.objects.filter(
            postCats__in=categories,
            postCreated__gte=last_week_start,
        )
        if new_articles:
            # Формируем список новых статей с гиперссылками
            article_list = "\n".join(
                [f"{article.postTitle}: [ссылка](http://127.0.0.1:8000{article.get_absolute_url()})" for article in new_articles])
            # Отправляем уведомление на почту
            subject = "Список новых статей за неделю от [newspaper.com]"
            message = f"Привет, {subscription.subscriptionUser.username}!\n\n" \
                      f"Новые статьи по любимой тематике за последюнюю неделю:\n{article_list}"
            from_email = settings.DEFAULT_FROM_EMAIL
            #recipient_list = [user_email]
            recipient_list = [subscription.subscriptionUser.email]  # Используем электронную почту пользователя из подписки

            send_mail(subject, message, from_email, recipient_list)

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
