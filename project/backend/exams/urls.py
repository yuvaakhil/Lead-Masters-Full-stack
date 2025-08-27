from django.urls import path
from . import views

urlpatterns = [
    path('available/', views.available_exams, name='available_exams'),
    path('<int:exam_id>/start/', views.start_exam, name='start_exam'),
    path('session/<uuid:session_id>/questions/', views.get_exam_questions, name='get_exam_questions'),
    path('session/<uuid:session_id>/answer/', views.submit_answer, name='submit_answer'),
    path('session/<uuid:session_id>/submit/', views.submit_exam, name='submit_exam'),
    path('session/<uuid:session_id>/result/', views.get_exam_result, name='get_exam_result'),
    path('history/', views.user_exam_history, name='user_exam_history'),
]