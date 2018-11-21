from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:category_pk>', views.blog_type, name='blog_type'),
    path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),
]