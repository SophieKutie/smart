import csv
import logging
from datetime import timedelta, datetime

import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.shortcuts import render
from django.template.defaultfilters import date

from smart.forms import UploadFileForm, TwitterhandlesForm

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


def get_uploaded(request):
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
