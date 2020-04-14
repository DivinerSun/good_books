from django.urls import path

from platforms.views import account

urlpatterns = [
    path('sms/send/', account.sms_send, name='sms_send'),
    path('register/', account.register, name='register'),
]
