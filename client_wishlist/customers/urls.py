from django.urls import path

from customers import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('customers/', views.CustomerList.as_view()),
    path('customers/<int:customer_id>/', views.CustomerDetail.as_view()),
]