# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import atcfinals.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(help_text=b'Specify when this event started')),
                ('end_date', models.DateField(help_text=b'Specify when this event ended')),
                ('description', models.CharField(help_text=b'In not more than 500 words, describe this experience', max_length=500)),
                ('skills_learnt', models.CharField(help_text=b'In less than 50 words, summarize what skills you gained through this event', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('identifier', models.AutoField(serialize=False, primary_key=True)),
                ('idea_name', models.CharField(help_text=b'What is the name of your idea?', max_length=40)),
                ('idea_bio_short', models.CharField(help_text=b'In less than 50 characters, summarize your idea', max_length=50)),
                ('idea_bio_long', models.CharField(help_text=b'Give a description of your idea in less than 500 words', max_length=500)),
                ('idea_webiste', models.URLField(help_text=b'Does your idea have a website?', null=True, blank=True)),
                ('is_public', models.BooleanField(help_text=b'Specify whether this idea will be public if true or only accessible by registered users')),
                ('created_at', models.DateTimeField(help_text=b'When this idea was added to the system', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text=b'When this idea was last updated', auto_now_add=True)),
                ('category', models.CharField(help_text=b'Choose a category for your idea', max_length=20, choices=[(b'Education', b'Education'), (b'Technology', b'Technology'), (b'Finance', b'Finance'), (b'Agriculture', b'Agriculture')])),
                ('likes', models.IntegerField(default=0, help_text=b'Number of likes that this has. Only registed users can like', editable=False)),
                ('comments', models.IntegerField(default=0, help_text=b'Number of comments that this idea has. Only registered users can comment', editable=False)),
                ('views_known', models.IntegerField(default=0, help_text=b'Number of views that this idea has from registered users', editable=False)),
                ('views_unknown', models.IntegerField(default=0, help_text=b'Number of view from anonymous users', editable=False)),
                ('idea_image', models.ImageField(null=True, upload_to=atcfinals.models.user_profile_image_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IdeaComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'Date and time of first comment', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text=b'Date and time of last update', auto_now=True)),
                ('comment_text', models.CharField(help_text=b'Comment in less than 150 characters', max_length=150)),
                ('idea_relation', models.ForeignKey(help_text=b'Idea being commented on', to='atcfinals.Idea')),
                ('user_relation', models.ForeignKey(help_text=b'User who is commenting on the idea', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IdeaLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'When this idea was liked by this user', auto_now_add=True)),
                ('idea_relation', models.ForeignKey(help_text=b'Idea being liked', to='atcfinals.Idea')),
                ('user_relation', models.ForeignKey(help_text=b'Registered user who is liking the idea', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IdeaView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text=b'Time and date when this user viewed this idea', auto_now_add=True)),
                ('idea_relation', models.ForeignKey(help_text=b'Idea being viewed', to='atcfinals.Idea')),
                ('user_relation', models.ForeignKey(help_text=b'Registered user who is viewing this idea', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Innovator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('innovator_name', models.CharField(help_text=b'Enter you name here', max_length=40)),
                ('innovator_email', models.EmailField(help_text=b'Enter you email address', max_length=254)),
                ('innovator_bio_short', models.CharField(help_text=b'Tell about you in less than 50 characters', max_length=50)),
                ('innovator_bio_long', models.CharField(help_text=b'Give us a summary about yourself', max_length=500)),
                ('innovator_location', models.CharField(help_text=b'Where are you located?', max_length=30)),
                ('innovator_webiste', models.URLField(help_text=b'If you have a website or blog, please add the link here', null=True, blank=True)),
                ('views', models.IntegerField(default=0, help_text=b'Number of views this profile has', editable=False)),
                ('created_at', models.DateTimeField(help_text=b'When this profile was created', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text=b'When this Innovator profile was last updated', auto_now=True)),
                ('innovator_picture', models.ImageField(null=True, upload_to=atcfinals.models.user_profile_image_path, blank=True)),
                ('user_relation', models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text=b'Link Innovator to existing user account')),
            ],
        ),
        migrations.AddField(
            model_name='idea',
            name='innovator_relation',
            field=models.ForeignKey(help_text=b'Which innovator owns this idea?', to='atcfinals.Innovator'),
        ),
        migrations.AddField(
            model_name='experience',
            name='innovator_relation',
            field=models.ForeignKey(help_text=b'Innovator creating this experience event', to='atcfinals.Innovator'),
        ),
        migrations.AlterUniqueTogether(
            name='idealike',
            unique_together=set([('user_relation', 'idea_relation')]),
        ),
    ]
