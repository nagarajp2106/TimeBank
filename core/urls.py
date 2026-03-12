from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('dashboard/learner/', views.learner_dashboard, name='learner_dashboard'),

    # Courses
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    # Enrollment
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('enrollment/<int:enrollment_id>/manage/', views.manage_enrollment, name='manage_enrollment'),

    # Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),

    # My Courses
    path('my-courses/', views.my_courses, name='my_courses'),

    # Wallet
    path('wallet/', views.wallet_view, name='wallet'),
]
