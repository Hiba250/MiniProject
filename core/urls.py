from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import review_feedback_view
from .views import complete_profile_view
from .views import all_traveler_plans_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    

    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('traveler-details/', views.traveler_profile_view, name='traveler_profile'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('travelplan/', views.create_plan_view, name='create_plan'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('update-location/', views.update_location_view, name='update_location'),
    path('user-details/', views.user_profile_view, name='user_profile'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    path('moderate-posts/', views.moderate_posts_view, name='moderate_posts'),
    path('locations/', views.location_list_view, name='location_list'),
    path('my-reports/', views.my_reports_view, name='my_reports'),
    path('review-feedback/', views.review_feedback_view, name='review_feedback'),  # ✅ Keep only one
    path('my-feedback/', views.my_feedback_view, name='my_feedback'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.traveler_dashboard_view, name='traveler_dashboard'),
    path('user-dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('explore/', views.explore_view, name='explore'),
    path('posts/', views.all_posts_view, name='all_posts'),
    
    path('edit-traveler/<int:traveler_id>/', views.admin_edit_traveler_view, name='admin_edit_traveler'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('complete-profile/', views.complete_profile_view, name='complete_profile'),
    path('my_index_view/', views.my_index_view, name='my_index_view'),
    path('my-plans/', views.my_plans_view, name='my_plans'),
    path('travelplan/', views.create_plan_view, name='create_plan'),
    path('suggest-plan/', views.create_suggestion_view, name='create_suggestion'),
    path('explore-plans/', all_traveler_plans_view, name='explore_plans'),
    path('manage-user/', views.manage_user_view, name='manage_user')


    # path('my-suggestions/', user_suggestions_view, name='user_suggestions'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

