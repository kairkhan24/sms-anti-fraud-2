from django.urls import path

from hrm.views import SendSmsMessageApi

urlpatterns = [
    path('send-sms-message/', SendSmsMessageApi.as_view())
]
