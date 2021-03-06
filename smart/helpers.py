import csv
import logging
from datetime import timedelta, datetime

import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.shortcuts import render

from django.http import HttpResponseRedirect

from smart.forms import UploadFileForm, TwitterhandlesForm, SearchForm, DateForm

logger = logging.getLogger(__name__)


# def get_durtion():
def get_duration_of_search():
    now = datetime.now()
    print("Today's date: ", str(now))

    # add 7 days to current date for live streaming duration
    live_search = now + timedelta(days=7)
    if live_search:
        print('Live search duration: ', timedelta(days=7), ' and ends: ', live_search)
        return 'Live search duration: ', timedelta(days=7), ' and ends: ', live_search

    # subtract 2 weeks from current date for retro
    retro = now - timedelta(weeks=2)
    if retro:
        print('Date two weeks ago: ', retro)


# print('two_weeks_ago object type: ', type(two_weeks_ago))


def get_hate_terms_from_file_system(csv_file_name: str) -> list:
    result = []
    if csv_file_name:
        try:
            csv_file = pd.read_csv(csv_file_name, encoding='utf')
            csv_file.drop_duplicates(keep='first', inplace=True)
            result = csv_file['terms'].astype(str).values.tolist()
        except (FileNotFoundError, ValueError):
            logger.error(f"Invalid file or filepath submitted: {csv_file_name} not found")
        except KeyError:
            logger.error(f"Submitted file {csv_file_name} does not contain csv header `terms`")
    else:
        logger.error(f"{csv_file_name} file or filepath is empty")

    return result



# def file_handler(request):
#     incomingfile = request.FILES['file']
#     default_storage.save("./test/data/user_handles/", ContentFile(incomingfile.read()))


def do_uploaded(request):
    aform = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES["myfile"]
        print(myfile)
        fs = FileSystemStorage()  # save path to be saved
        print(fs)
        filename = fs.save(myfile.name,    myfile)  # save file name and file
        uploaded_file_url = fs.url(filename)
    else:
        aform = TwitterhandlesForm(request.POST)
    return render(request, 'twitter_handles_form.html', {'aform': aform})



def get_date(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        dform = DateForm(request.POST)
        # check whether it's valid:
        if dform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return 'thanks'

    # if a GET (or any other method) we'll create a blank form
    else:
        dform = DateForm()

    return render(request, 'twitter_handles_form.html', {'dform': dform})


def do_uploaded_for_terms(request):
    bform = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST' and request.FILES['hatefile']:
        hatefile = request.FILES["hatefile"]
        print(hatefile)
        fs = FileSystemStorage(location='./test/data/abusive_terms')  # save path to be saved
        print(fs)
        # filename = fs.save(hatefile.name,  hatefile)  # save file name and file
        # uploaded_file_url = fs.url(filename)
    else:
        bform = SearchForm(request.POST)
    return render(request, 'model_form_upload.html', {'bform': bform})


def time_format():

    # s = datepicker_value[0,1]
    dateFile = open('test/data/datefile.csv', 'w', newline='')
    wr = csv.writer(dateFile)
    wr.writerow()
