import logging

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .forms import SearchForm

logger = logging.getLogger(__name__)

#
# class Home(TemplateView):
#     template_name = 'home.html'


def index(request):
    ''' template = loader.get_template('smart/home.html')
    return HttpResponse(template) '''
    return render(request, 'smart/home.html')


def contact(request):
    return render(request, 'smart/goingtwitter.html',
                  {'content': ['if you would like to contact me, email me', '@sunderland']})


def goingtwitter(request):
    return render(request, 'smart/goingtwitter.html')


def search(request):
    # return render(request, 'smart/model_form_upload.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('index')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'smart/model_form_upload.html', {"form": form})


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

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
