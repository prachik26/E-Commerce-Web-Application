from django.urls import path
from website.views import Signup
from website.views import LoginUser
from website import views
urlpatterns=[
    path('',views.home, name="base"),
    path('login/', LoginUser.as_view(), name="login"),
    path('register/', Signup.as_view(), name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('store/', views.welcome, name="store"),
    path('cart/', views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update_item"),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.processOrder, name="process_order"),
    path('success/', views.success, name="success"),
]