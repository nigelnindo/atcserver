# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageTests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=api.models.test_image_path)),
                ('image_description', models.CharField(help_text=b'Describe this image', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(help_text=b'Enter your question here.', max_length=500)),
                ('created_at', models.DateTimeField(help_text=b'This is when this question was created', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text=b'This is when this question was last updated', auto_now=True)),
                ('user_relation', models.ForeignKey(help_text=b'User who created the question.', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'When this comment was added to the system', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment_text', models.CharField(help_text=b'Comment on a question', max_length=300)),
                ('question_relation', models.ForeignKey(help_text=b'The question being commented on', to='api.Question')),
                ('user_relation', models.ForeignKey(help_text=b'The user who is making a comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(help_text=b'Give a summary of your individual expertise.', max_length=200)),
                ('user_relation', models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text=b'Link to user profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(help_text=b'Link to uploaded picture', upload_to=api.models.user_profile_image_path)),
                ('image_description', models.CharField(default=b'No description provided.', help_text=b'Describe this image', max_length=100)),
                ('owner', models.ForeignKey(help_text=b'Who uploaded the picture', to='api.UserProfile')),
            ],
        ),
    ]
