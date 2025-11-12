from django.urls import path
from . import views

app_name = 'architects'

urlpatterns = [
    path('register/', views.register_architect, name='architect_register'),
    path('edit/', views.edit_architect, name='architect_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reviews/', views.review_applications, name='review_applications'),
    path('review/<int:review_id>/', views.process_review, name='process_review'),
    path('payment/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('certificate/', views.generate_certificate, name='generate_certificate'),
]
