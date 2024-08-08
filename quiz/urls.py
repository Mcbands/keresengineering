from django.urls import path
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,)

app_name= 'quiz'


urlpatterns = [
    # path('main/<int:course_id>/', QuizListView.as_view(), name='main'),
    path('main/', QuizListView.as_view(), name='main'),
    path('main/<int:pk>/', quiz_view, name='quiz_view'),
    path('main/<int:pk>/save/', save_quiz_view, name='save_view'),
    path('main/<int:pk>/data/', quiz_data_view, name='quiz_data_view'),
]


