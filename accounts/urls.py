from django.urls import path
from . import views

urlpatterns = [
    path('send-code/', views.UserLogin.as_view(), name='send_code'),
    path('verify-code/', views.ChekOtp.as_view(), name='verify_code'),
    path('nameuser/', views.CompleteProfileView.as_view(), name='nameuser'),
    path('otplogin/', views.OtpLoginView.as_view(), name='OtpLogin'),

]
