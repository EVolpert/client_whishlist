from django.urls import path

from whishlist import views

urlpatterns = [
    path('customers/<int:customer_id>/whishlist', views.WhishListDetailView.as_view()),
]