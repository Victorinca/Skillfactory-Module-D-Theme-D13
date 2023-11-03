# Generated by Django 4.2.7 on 2023-11-02 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0015_comment_comment_is_accepted_alter_post_postauthor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postAuthor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
