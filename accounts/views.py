import uuid
from random import randint
from .models import User, Otp
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect, reverse
from uuid import uuid4
from django.views import View
from .forms import LogimForm, RegisterForm, ChekOtpForm, CompeletProfile
import requests
import json
from django.utils.crypto import get_random_string

# SMS = ghasedak_sms.Ghasedak('35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz')


# sms_api = ghasedak_sms.Ghasedak("35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz",
#                                 'https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams')

API_KEY = "35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz"  # کلید API خود را وارد کنید


class UserLogin(View):
    def get(self, request, *args, **kwargs):
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


class OtpLoginView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'accounts/otplogin.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            phone = cd['phone']
            send_otp(phone, randcode)
            token = str(uuid4())

            print(randcode)
            print(send_otp)

            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)

            return redirect(reverse('verify_code') + f'?token={token}')
        else:
            form.add_error('phone', 'شماره تلفن صحیح نیست')
        return render(request, 'accounts/otplogin.html', {'form': form})


class ChekOtp(View):
    def get(self, request, *args, **kwargs):
        form = ChekOtpForm()
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = ChekOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                if otp:
                    user, created = User.objects.get_or_create(phone=otp.phone)
                    if not user.first_name or not user.last_name:
                        return redirect(reverse('nameuser') + f'?token={token}')

                login(request, user)
                otp.delete()
            else:
                return redirect('/')
        return render(request, 'accounts/verify_code.html', {'form': form})


class CompleteProfileView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            try:
                otp = Otp.objects.get(token=token)
                phone = otp.phone
                form = CompeletProfile()
                return render(request, 'accounts/name.html', {'form': form, 'phone': phone, 'token': token})
            except Otp.DoesNotExist:
                return redirect('/')  # اگر توکنی با این مقدار یافت نشد، به صفحه اصلی هدایت می‌شود
        else:
            return redirect('/')  # در صورتی که توکن موجود نباشد، به صفحه اصلی هدایت می‌شود

    def post(self, request):
        token = request.GET.get('token')
        if token:
            try:
                otp = Otp.objects.get(token=token)
                phone = otp.phone
                form = CompeletProfile(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    user = User.objects.get(phone=phone)
                    user.first_name = cd['first_name']
                    user.last_name = cd['last_name']
                    user.save()  # ذخیره تغییرات در دیتابیس
                    login(request, user)
                    otp.delete()  # پس از تکمیل پروفایل، توکن را حذف کنید
                    return redirect('/')
                else:
                    return render(request, 'accounts/name.html', {'form': form, 'phone': phone, 'token': token})
            except Otp.DoesNotExist:
                return redirect('/')  # در صورتی که توکن معتبر نباشد
        return redirect('/')


def NameUser(request):
    user = User.objects.all()
    return render(request, 'base.html', {'user': user})


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
