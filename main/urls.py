from django.urls import path
from main import views 


urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('pay/', views.pay, name='pay'),
    path('dashboard/home/', views.dashboard_home, name='dashboard-home'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/courses-enrolled/', views.courses_enrolled, name='courses-enrolled'),
    path('dashboard/courses-uploaded/', views.courses_uploaded, name='courses-uploaded'),
    path('dashboard/upload/', views.upload, name='upload'),
    path('dashboard/<slug:slug>/course-edit/', views.course_edit, name='course-edit'),
    path('dashboard/<slug:slug>/delete/', views.delete_course, name='delete-course'),
    path('<str:instructor>/course/<slug:slug>/', views.course_details, name='course_details'),
    path('courses/<str:category>/', views.category, name='category'),
    path('module_detail/<int:module_id>/', views.module_detail, name='module_detail'),
    path('dash/<int:course_id>/', views.dash, name='dash'),
    path('dash/', views.dash, name='dash_no_id'),
    path('error_404/', views.error_404, name='error_404'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),


    path('dash/<int:course_id>/', views.redirect_dash, name='redirect_dash'),
    path('dash/', views.redirect_dash_no_id, name='redirect_dash_no_id'),
    path('dashboard/', views.dash, name='dash'),

]




