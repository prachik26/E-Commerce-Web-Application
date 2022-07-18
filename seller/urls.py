from django.urls import path
from seller.views import SignupSeller, LoginSeller
from seller import views
urlpatterns=[
    
    path('seller_login/', LoginSeller.as_view(), name="seller_login"),
    path('seller_register/', SignupSeller.as_view(), name="seller_signup"),
    path('logout/', views.logout_user, name="logout"),
    path('seller_product/', views.viewProduct, name="seller_product"),
    path('seller_add-product/', views.add_product, name="seller_add-product"),
]