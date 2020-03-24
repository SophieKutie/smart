from django.contrib import admin

from .models import Question, Choice, Document, TodoItem

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Document)
admin.site.register(TodoItem)
