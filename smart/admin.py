from django.contrib import admin

from .models import Question, Choice, Post, Document, TodoItem, Category

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Document)
admin.site.register(TodoItem)
admin.site.register(Category)
admin.site.register(Post)
