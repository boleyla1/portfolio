import ghasedak_sms

# ایجاد شیء Ghasedak با کلید API
SMS = ghasedak_sms.Ghasedak('35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz')

# ارسال کد تایید (OTP) به شماره تلفن
response = SMS.verification({
    'receptor': '09965759902',
    'type': '1',  # نوع پیام: 1 برای SMS و 2 برای تماس صوتی
    'template': 'Ghasedak',
    'param1': '1234'  # کد OTP
})

# بررسی وضعیت SMS
try:
    sms_status = SMS.check_sms_status()
    print("SMS Status:", sms_status)
except Exception as e:
    print("An error occurred:", str(e))
