from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'smart'
urlpatterns = [

    # ex: /smart/
    path('', views.index, name='index'),

    # ex:
    # path('', views.index, name='index'),

    # # ex: /smart/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    #
    # # ex: /smart/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    #
    # # ex: /smart/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),

    path('search/', views.search, name='search'),

    path('goingtwitter/', views.goingtwitter, name='goingtwitter'),

    path('contact/', views.contact, name='contact'),

    # path('search/<misogynistic>', views.search),
    #
    # path('search/<racist>', views.search),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
