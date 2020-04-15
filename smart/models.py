import datetime
import os
from django.conf import settings

from django import forms
from django.contrib.staticfiles import storage
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)

# class MyStaticFilesStorage(storage.StaticFilesStorage):
#     def __init__(self, *args, **kwargs):
#         kwargs['file_permissions_mode'] = 0o640
#         kwargs['directory_permissions_mode'] = 0o760
#         super().__init__(*args, **kwargs)

import logging

logging.basicConfig(filename='file.log', level=logging.DEBUG, format='%(levelname)s:%(message)s')


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='../media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):  # __unicode__ on Python 2
    #     return self.pub_date >= timezone.now() - \
    #            datetime.timedelta(days=1)


class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - \
               datetime.timedelta(days=1)


class Choice(models.Model):
    # ...
    def __str__(self):  # __unicode__ on Python 2
        return self.choice_text


class TodoItem(models.Model):
    content = models.TextField()


class Category(models.Model):
    choices = [
        ('misogynistic', 'misogynistic'),
        ("racist", "racist"),
        ("homophobic", "homophobic")
    ]

    name = models.CharField(max_length=200, choices=choices)


class Post(models.Model):
    # post = models.CharField(max_length=500)
    csv = models.FileField(upload_to='hate_speech')
    categories = models.ManyToManyField(Category, blank=True, default=None)

    # user = models.ForeignKey('User', on_delete=models.PROTECT)

    def __str__(self):  # __unicode__ on Python 2
        return self.csv




