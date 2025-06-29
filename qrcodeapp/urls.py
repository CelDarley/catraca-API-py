from django.urls import path
from .views import QRCodeRegisterView, QRCodeListView, QRCodeDeleteView

urlpatterns = [
    path('register/', QRCodeRegisterView.as_view(), name='register-qrcode'),
    path('list/', QRCodeListView.as_view(), name='list-qrcodes'),
    path('delete/', QRCodeDeleteView.as_view(), name='delete-qrcode'),
] 