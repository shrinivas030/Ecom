from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('register/',views.registerpage,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),

    path('user/',views.userpage,name='user'),
    path('accountsetting/',views.accountSetting,name='accountsetting'),


    path('products/',views.products,name='products'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    path('createorder/<str:pk_test>/',views.create_Order,name='createorder'),
    path('update_order/<str:pk_test>/',views.updateOrder,name='update_order'),
    path('delete_order<str:pk_test>/',views.deleteOrder,name='delete_order'),

    path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name='reset_password_sent'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset_password_comlete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_done'),
]