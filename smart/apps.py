from django.apps import AppConfig
from flask import Flask, render_template, request, app


class SMARTConfig(AppConfig):
    name = 'smart'


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         print(request.form.getlist('category'))
#         return 'Done'
#     return render_template('model_form_upload.html')
