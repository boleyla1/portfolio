from random import randint
from .models import User, Otp
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect, reverse
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
import ghasedak_sms
from .forms import LogimForm, RegisterForm, ChekOtpForm
import requests
import json
import ghasedak_sms

# SMS = ghasedak_sms.Ghasedak('35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz')


# sms_api = ghasedak_sms.Ghasedak("35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz",
#                                 'https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams')

API_KEY = "35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz"  # کلید API خود را وارد کنید


class UserLogin(View):
    def get(self, request):
        form = LogimForm()
        return render(request, 'accounts/send_code.html', {'form': form})

    def post(self, request):
        form = LogimForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('phone', 'شماره تلفن است')
        else:
            form.add_error('phone', 'شماره تلفن است')

        return render(request, 'accounts/send_code.html', {'form': form})


class RigesterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            phone = cd['phone']
            # sms_api.verification({'receptor': phone, 'type': '1', 'template': 'boleyla', 'param1': randcode})
            send_otp(phone, randcode)

            print(randcode)
            print(send_otp)

            Otp.objects.create(phone=cd['phone'], code=randcode)

            return redirect(reverse('verify_code') + f'?phone={cd['phone']}')
        else:
            form.add_error('phone', 'شماره تلفن صحیح نیست')
        return render(request, 'accounts/register.html', {'form': form})


class ChekOtp(View):
    def get(self, request):
        form = ChekOtpForm()
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        phone = request.GET.get('phone')
        form = ChekOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], phone=phone).exists():
                user = User.objects.create_user(phone=phone)
                login(request, user)
                print(user)
                return redirect('/')
            else:
                return redirect('register')
        return render(request, 'accounts/verify_code.html', {'form': form})


def NameUser(request):
    return render(request, 'accounts/name.html')


#----------- پنل پیامکی-----------------
def send_otp(mobile, param1, ):
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams"

    print(f"Sending OTP to: {mobile}, Code: {param1}")

    payload = json.dumps({
        "receptors": [
            {
                "mobile": str(mobile),
                "clientReferenceId": "1"
            }
        ],
        "templateName": "boleyla",
        "param1": str(param1),
        "isVoice": False,
        "udh": False
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def send_welcome_sms_if_new_user(phone):
    # چک کردن که آیا شماره تلفن قبلاً ثبت شده است

    # اگر شماره تلفن جدید باشد، پیام خوشامدگویی ارسال می‌کنیم
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams"

    # پیام خوشامدگویی
    message = ("🌟 خوش آمدید به دنیای مهرشاد بلیلا! 🌟\nبا ورود شما به این سایت، به جمع کسانی پیوسته‌اید که همیشه در "
               "جستجوی بهترین‌ها هستند.")

    payload = json.dumps({
        "receptors": [
            {
                "mobile": str(phone),
                "clientReferenceId": "1"
            }
        ],
        "templateName": "boleyla",  # اگر نام قالب متفاوت است، اینجا تغییر دهید
        "param1": message,  # پیام خوشامدگویی
        "isVoice": False,
        "udh": False
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': API_KEY  # کلید API خود را وارد کنید
    }

    response = requests.post(url, headers=headers, data=payload)

    print("Response Status:", response.status_code)
    print("Response Data:", response.text)

    return response.json()  # در صورت موفقیت می‌توانید پیغام را برگشت دهید یا تصمیم‌گیری کنید
