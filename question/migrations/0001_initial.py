# Generated by Django 3.2 on 2021-05-03 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_question_related', to=settings.AUTH_USER_MODEL)),
                ('downvote', models.ManyToManyField(blank=True, related_name='question_question_down', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank=True, related_name='favorited_users', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('upvote', models.ManyToManyField(blank=True, related_name='question_question_up', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_comment_related', to=settings.AUTH_USER_MODEL)),
                ('downvote', models.ManyToManyField(blank=True, related_name='question_comment_down', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commented_question', to='question.question')),
                ('upvote', models.ManyToManyField(blank=True, related_name='question_comment_up', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('accepted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answer_related', to=settings.AUTH_USER_MODEL)),
                ('downvote', models.ManyToManyField(blank=True, related_name='question_answer_down', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answered_question', to='question.question')),
                ('upvote', models.ManyToManyField(blank=True, related_name='question_answer_up', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
