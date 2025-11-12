from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('<int:payment_id>/', views.payment_detail, name='detail'),
    path('<int:payment_id>/process/', views.process_payment, name='process'),
    path('certificate/download/', views.download_certificate, name='download_certificate'),
]