from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),

    path('', views.dashboard, name='dashboard'),
    path('user/', views.userpage, name='user-page'),
    path('products/', views.products, name='products'),
    path('costumer/<str:pk>/', views.costumer, name='costumer'),  # <str:pk> tag that get id of costumer, dynamic url
    path('delete_costumer/<str:pk>/', views.deletecostumer, name="delete_costumer"),

    path('create_order/', views.createorder, name='create_order'),
    path('update_order/<str:pk>/', views.updateorder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteorder, name="delete_order"),

    path('new_products/', views.newproducts, name="new_products"),

    path('home/', views.home, name="home"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_Item/', views.updateItem, name="update_Item"),
    path('product_details/', views.productDetails, name="product_details")

]
