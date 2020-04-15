from django import forms

from .models import Document
from .utilities.widgets import BootstrapDateTimePickerInput

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

    t_h_canned = forms.FilePathField(path="media/")
    canned_field = forms.FilePathField(path="smart/category/")


MAPPING = {
    "1": "category/racisttest.csv",
    "2": "category/miso.csv",
    "3": "category/homo.csv",

}
CHOICES = (
    ("1", "Racist terms"),
    ("2", "Misogynistic terms"),
    ("3", "Homo terms"),

)


class TwitterhandlesForm(forms.Form):
    handles_upload = forms.FileField(required=False, allow_empty_file=False,
                                     widget=forms.ClearableFileInput(attrs={'multiple': True}))

    handles_typed = forms.CharField(widget=forms.Textarea, required=False)

    handles_category = forms.FilePathField(path="media/", required=False)





class SearchForm(forms.Form):


    # category = forms.MultipleChoiceField(choices=CHOICES, required=False)
    uploaded = forms.FileField(required=False, allow_empty_file=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    typed = forms.CharField(widget=forms.Textarea, required=False)

    category = forms.FilePathField(path="smart/category/", required=False)



# class FilePathFieldForm(forms.Form):
#     file_field = forms.FileField(widget=forms .ClearableFileInput(attrs={'multiple': True}))

