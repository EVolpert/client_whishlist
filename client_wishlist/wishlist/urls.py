from django.urls import path

from wishlist import views

urlpatterns = [
    path('customers/<int:customer_id>/wishlist', views.WishListDetailView.as_view()),
    path('customers/<int:customer_id>/wishlist/<str:product_id>', views.WislistUpdateView.as_view()),
]