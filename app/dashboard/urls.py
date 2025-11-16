from django.urls import path
from . import views

urlpatterns = [
        path('', views.dashboard_view, name='dashboard'),
        path('calendar/', views.calendar_view, name='dashboard_calendar'),
        path('exams/', views.exams_view, name='dashboard_exams'),
        path('materials/', views.materials_view, name='dashboard_materials'),
        path('courses/', views.courses_view, name='dashboard_courses'),
]
