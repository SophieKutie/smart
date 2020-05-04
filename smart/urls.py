from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'smart'
urlpatterns = [

    # ex: /smart/
    path('', views.index, name='index'),

    path('search/', views.search, name='search'),

    path('handles_search/',  views.handles_search, name='handles_search'),

    path('goingtwitter/', views.goingtwitter,  name='goingtwitter'),

    path('goingtwittertwo/', views.goingtwittertwo,  name='goingtwittertwo'),

    path('contact/', views.contact, name='contact'),



    # path('search/<misogynistic>', views.search),
    #
    # path('search/<racist>', views.search),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
