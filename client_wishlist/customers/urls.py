from django.urls import path

from customers import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('csrf', views.csrf, name='csrf'),
    path('customers/', views.CustomertList.as_view()),
    path('customers/<int:customer_id>/', views.CustomerDetail.as_view()),
]