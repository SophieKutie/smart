from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Post, User

from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


DEMO_CHOICES = (
    ("1", "Racist terms"),
    ("2", "Misogynistic terms"),
    ("3", "Homo terms"),

)

class SearchForm(forms.Form):
    canned = forms.MultipleChoiceField(choices=DEMO_CHOICES, required=False)
    uploaded = forms.FileField(required=False)
    typed = forms.CharField(widget=forms.Textarea, required=False)


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))