from django.urls import path, re_path
from . import views

urlpatterns = [
    path('wblog/', views.blog_list, name='blogs'),
    re_path(r'^blog/(?P<slug>[\w\u0600-\u06FF-]+)/$', views.blog_detail, name="blog_detail"),  # پشتیبانی از فارسی
]
