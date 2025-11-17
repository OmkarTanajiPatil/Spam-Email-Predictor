from django.urls import path

from .views import MailClassifierView

urlpatterns = [
    path('', MailClassifierView.as_view(), name='mail-form'),
]
