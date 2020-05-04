from django import forms

from .models import Document, DateForm
from .utilities.widgets import BootstrapDateTimePickerInput
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms


# class EventForm(forms.ModelForm):
#     class Meta:
#         # l = Event
#         fields = ['name', 'start_date', 'end_date', 'start_time', 'end_time']
#         widgets = {
#             'start_date': DatePickerInput().start_of('event days'),
#             'end_date': DatePickerInput().end_of('event days'),
#             'start_time': TimePickerInput().start_of('party time'),
#             'end_time': TimePickerInput().end_of('party time'),
#         }


class DateForm(forms.DateInput):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


class Meta:
    model = DateForm
    fields = ["date", ]


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
        # upload_to='../test/data/user_handles/')

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

MAPPING_1 = {
    "1": "./test/data/20200415-011333_tweets.json",
    "2": "./test/data/20200415-011333_tweets.json ",
    "3": "./test/data/20200415-011333_tweets.json",

}

CHOICES_1 = (
    ("1", "#meghan2020/04/15"),
    ("2", "#"),
    ("3", "#"),

)





# def get_now():
#     return datetime.now().strftime("%d/%m/%Y %H:%M")

class TwitterhandlesForm(forms.Form):
    handles_upload = forms.FileField(required=False, allow_empty_file=False,
                                     widget=forms.ClearableFileInput(attrs={'multiple': True}))

    handles_typed = forms.CharField(widget=forms.Textarea, required=False)

    handles_category = forms.FilePathField(path="media/", required=False)

    # date = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #     })
    # )


class SearchForm(forms.Form):
    uploaded = forms.FileField(required=False, allow_empty_file=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    typed = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.FilePathField(path="smart/category/", required=False)
    # returned_handle_tweets_file = forms.FilePathField(path="./test/data/", required=False)