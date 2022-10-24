from django.urls import path
from .import views

urlpatterns = [
     path('',views.home,name='home'),
     path('signin',views.signin,name='signin'),
     path('signup',views.signup,name='signup'),
     path('logout',views.logout,name='logout'),
     path('add_category',views.add_category,name='add_category'),
     path('delete_category/<int:pk>',views.delete_category,name='delete_category'),
     path('show_category',views.show_category,name='show_category'),
     path('add_book',views.add_book,name='add_book'),
     path('show_book',views.show_book,name='show_book'),
     path('view_users',views.view_users,name='view_users'),
     path('delete_user/<int:pk>',views.delete_user,name='delete_user'),
     path('view_category',views.view_category,name='view_category'),
     path('view_book/<int:pk>',views.view_book,name='view_book'),
     path('delete_book/<int:pk>',views.delete_book,name='delete_book'),
     path('req_booking/<int:pk>',views.req_booking,name='req_booking'),
     path('view_booking',views.view_booking,name='view_booking'),
     path('edit_profile',views.edit_profile,name='edit_profile'),
     path('generateOTP',views.generateOTP,name='generateOTP'),
     path('admin_booking',views.admin_booking,name='admin_booking'),
     path('approve/<int:pk>',views.approve,name='approve'),
     path('reject_booking/<int:pk>',views.reject_booking,name='reject_booking'),



]