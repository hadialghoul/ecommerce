from django.urls import path
from .import views



urlpatterns=[
path('',views.store,name='store'),
path('product/<slug:slug>/',views.product_info,name='product-info'),
path('search/<slug:slug>/',views.category_list,name='category-list'),

]