import csv
import logging
from io import StringIO

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.urls import reverse

from scripts import twitterlive
from .forms import TwitterhandlesForm, SearchForm, UploadFileForm, DocumentForm
from .helpers import get_hate_terms_from_file_system, get_uploaded
    # file_handler
from pathlib import Path
from datetime import datetime, date, timedelta

# from .scripts import twitter

logger = logging.getLogger(__name__)
QUERY_TIME_LIMIT = 10


def index(request):
    ''' template = loader.get_template('smart/home.html')
    return HttpResponse(template) '''
    return render(request, 'smart/home.html')


def contact(request):
    return render(request, 'smart/contact.html',
                  {'content': ['if you would like to contact me, email me', '@sunderland']})


# def get_duration_of_search(request):
#     now = datetime.now()
#     print("Today's date: ", str(now))
#
#     # add 7 days to current date for live streaming duration
#     live_search = now + timedelta(days=7)
#     if live_search:
#         print('Live search duration: ', timedelta(days=7), ' and ends: ', live_search)
#         return 'Live search duration: ', timedelta(days=7), ' and ends: ', live_search
#
#     # subtract 2 weeks from current date for retro
#     retro = now - timedelta(weeks=2)
#     if retro:
#         print('Date two weeks ago: ', retro)


# return render(request, 'smart/goingtwitter.html', {'date': date})


def goingtwitter(request):
    # data = twitterlive.run_script()
    # print(data)

    return render(request, 'smart/goingtwitter.html')


def goingtwittertwo(request):
    data = twitterlive.run_script()
    print(data)

    return render(request, 'smart/goingtwittertwo.html')


def create_twitter_query_using_form_1(handles_upload, handles_typed, handles_example) -> dict:
    """
    Creates a dictionary representing a query that will be used to query twitters api.
    """
    query = {'terms': []}
    # if query object gets to more than 3 keys, transform into a class

    if handles_example:
        # open up a file on the server here
        # https://realpython.com/working-with-files-in-python/
        # use the choice number to identify the file to load
        # pass
        #
        get_hate_terms_from_file_system(handles_example)
        #file_handler(handles_example)

    if handles_typed:
        # split the contents of .typed and transform into a list
        # pass
        # transform to csv file too and place in directory user_handles
        query['terms'] = get_hate_terms_from_file_system(StringIO(handles_typed))
        outputFile = open('test/data/abusive_terms/typed_output.csv', 'w', newline='')
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(query['terms'])

    if handles_upload:
        # open up a file from the client here
        # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
        # read the file that was uploaded and transform into a  list
        # pass
        get_uploaded(handles_upload)

    # return query


# def create_twitter_query_using_form(category, typed, uploaded, date) -> dict:
#     """
#     Creates a dictionary representing a query that will be used to query twitters api.
#     """
#     query = {'terms': []}
#
#     # if query object gets to more than 3 keys, transform into a class
#
#     if category:
#         # open up a file on the server here
#         # https://realpython.com/working-with-files-in-python/
#         # use the choice number to identify the file to load
#         # pass
#         query['terms'] = get_hate_terms_from_file_system(category)
#
#     if typed:
#         # split the contents of .typed and transform into a list
#         # pass
#         query['terms'] = get_hate_terms_from_file_system(StringIO(typed))
#
#     if uploaded:
#         # open up a file from the client here
#         # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
#         # read the file that was uploaded and transform into a  list
#         # pass
#         query['terms'] = get_hate_terms_from_file_system(uploaded)
#
#     print(query)
#     return query


def handles_search(request):
    # template_name = 'smart/twitter_handles_form.html'
    # return render(request, 'smart/twitter_handles_form.html')
    # if this is a POST request we need to process the form data

    #
    aform = TwitterhandlesForm(request.POST)
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:

    # # testing picker post request 29/04/2020

    # print(datepicker_value[1])
    # print(request.POST['datetimes'])
    # collect the date value when its been sent to the server
    # datepicker_value = request.POST['datetimes'].replace(' ', ' ')
    #
    # # convert date string format to useable format for tweepy
    # datepicker_value = datetime.strptime(datepicker_value, '%Y/%m/%d-%Y/%m/%d').strftime('%Y-%m-%d')
    #
    # # seperate the string to give individual dates   ************seems to be reading start date as 2020 rather than whole string
    # #
    # datepicker_value = datepicker_value.split(' - ')
    # start_date1 = datepicker_value[0]
    # end_date1 = datepicker_value[1]

    # check whether it's valid:
        if aform.is_valid():
        # aform.save()
        # process the data in form.cleaned_data as required

            create_twitter_query_using_form_1(aform.cleaned_data['handles_example'],
                                          aform.cleaned_data['handles_typed'],
                                          request.FILES.get('handles_upload'))

    # return redirect('/search/')
    # # '?startdate=' + start_date1)
    # print("redirecting")

        return render(request, 'smart/model_form_upload.html')

    return render(request, 'smart/twitter_handles_form.html', {"aform": aform})


def search(request):
    # return render(request, 'smart/model_form_upload.html')
    # if this is a POST request we need to process the form data
    bform = SearchForm(request.POST)
    # getting startdate parameter on url
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    print(start_date)
    print(end_date)

    # create a form instance and populate it with data from the request:

    # testing picker post request
    # print(request.POST['datetimes'])

    # check whether it's valid:
    # if bform.is_valid():
    #     # process the data in form.cleaned_data as required
    #     query = create_twitter_query_using_form(bform.cleaned_data['category'],
    #                                             bform.cleaned_data['typed'],
    #                                             request.FILES.get('uploaded'),
    #                                             # aform.cleaned_data['handles_category'],
    #                                             # aform.cleaned_data['handles_typed'],
    #                                             # request.FILES.get('handles_upload')
    #
    #                                             )
    #     print(query)
    # ...
    # redirect to a new URL:
    # return redirect('/')

    ############# 02/05 ########## for submitting to folder
    # form = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST' and request.FILES['hatefile']:
        hatefile = request.FILES["hatefile"]
        print(hatefile)
        fs = FileSystemStorage(location='./test/data/abusive_terms')  # save path to be saved
        print(fs)
        filename = fs.save(hatefile.name, hatefile)

        # save output file data folder
        # output_file = f'./test/data/{datetime.now().strftime("%Y%m%d-%H%M%S")}_tweets.json'
        # # run script
        # twitterlive.run_script(0, 0, query['terms'], QUERY_TIME_LIMIT, output_file, reps=5)
        # , duration, start_date , finish_date)

        # tweet path to read from if tweets were fetched
        # tweets_path = Path("./test/data/tweets.json")
        # if tweets_path.exists():
        #     tweets = tweets_path.read_text()
        # else:
        #     logger.info("Unable to find file for tweets")
        #     tweets = ""

        # return render(request, 'smart/goingtwittertwo.html', {'terms': query['terms'], 'tweets': tweets})

        # if a GET (or any other method) we'll create a blank form

        return render(request, 'smart/goingtwittertwo.html')

    return render(request, 'smart/model_form_upload.html', {"bform": bform})

# class FileFieldView(FormView):
#     form_class = FileFieldForm
#     template_name = 'upload.html'  # Replace with your template.
#     success_url = '...'  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 ...  # Do something with each file.
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

# def upload(request):
#     context = {}
#
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         logging.INFO('not right')
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         context['url'] = fs.url(name)
#     return render(request, 'model_form_upload.html', context)
#

# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('smart.views.model_form_upload'))
#     else:
#         form = DocumentForm()
#
#         # Load documents for the list page
#     documents = Document.objects.all()
#
#     return render(request, 'smart/model_form_upload.html', {
#         'form': form
#     })

# def upload(request):
#     context = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         context['url'] = fs.url(name)
#     return render(request, 'model_form_upload.html', context)

# logger = logging.getLogger('project.smart')

# def upload(request):
#     if request.method == 'POST' and request.FILES.get('myfile', None):
#         logger.error('Something went wrong')
#         myfile = request.FILES.get("myfile", None)
#         fs = FileSystemStorage(location='/media/')
#         print(fs)
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         print("Sophie", uploaded_file_url.name)
#         print(uploaded_file_url.size)
#         return render(request, 'smart/model_form_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'smart/model_form_upload.html')

# handle_uploaded_file(myfile)

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form = handle_uploaded_file(request.FILES['form'])
#             form.save()
#             return HttpResponseRedirect('/smart/contact.html')
#         else:
#             form = UploadFileForm()
#
#     return render(request, 'smart/model_form_upload.html', {'form': form})
#
#
# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#             destination.close()

# def addTodo(request):
#     new_item = TodoItem(content=request.POST['content'])
#     new_item.save()
#     return HttpResponseRedirect('/newsearch/')
#
#
# def deleteTodo(request, todo_id):
#     item_to_delete = TodoItem.objects.get(id=todo_id)
#     item_to_delete.delete()
#     return HttpResponseRedirect('/todo/')
#
#
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
#
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# class NewSearchView(TemplateView):
#     template_name = 'smart/model_form_upload.html'
#
#     def get(self, request):
#         form = NewSearchForm()
#         return render(request, self.template_name, {'form': form})
#
#     # handling data sent to server
#     def post(self, request):
#         form = NewSearchForm(request.POST)
#         if form.is_valid():
#             form.save()
#             text = form.cleaned_data['post']
#             form = NewSearchForm()
#             return redirect('newsearch:newsearch')
#
#             args = {'form': form, 'text': text}
#             return render(request, self.template_name, args)
