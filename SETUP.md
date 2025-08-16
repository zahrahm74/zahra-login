# راهنمای راه‌اندازی Flask Application

## مراحل نصب و راه‌اندازی

### 1. پیش‌نیازها
- Python 3.8 یا بالاتر
- pip (مدیر بسته‌های Python)

### 2. نصب وابستگی‌ها
```bash
# ایجاد محیط مجازی
python3 -m venv venv

# فعال‌سازی محیط مجازی
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows

# نصب وابستگی‌ها
pip install -r requirements.txt
```

### 3. تنظیم متغیرهای محیطی
فایل `.env` را ویرایش کنید:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
```

### 4. اجرای سرور
```bash
# روش 1: اجرای مستقیم
python app.py

# روش 2: استفاده از اسکریپت راه‌اندازی
python run.py

# روش 3: استفاده از Flask CLI
flask run
```

### 5. دسترسی به اپلیکیشن
- رابط کاربری: http://localhost:5000
- API اطلاعات: http://localhost:5000/api
- بررسی وضعیت: http://localhost:5000/health

## تست اپلیکیشن

### تست ساده
```bash
python test_simple.py
```

### تست API
```bash
python test_api.py
```

### تست با curl
```bash
# بررسی وضعیت سرور
curl http://localhost:5000/health

# ثبت نام کاربر
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "first_name": "نام",
    "last_name": "نام خانوادگی"
  }'

# ورود کاربر
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123"
  }'
```

## ویژگی‌های امنیتی

### اعتبارسنجی رمز عبور
- حداقل 8 کاراکتر
- حداقل یک حرف بزرگ
- حداقل یک حرف کوچک
- حداقل یک عدد

### اعتبارسنجی نام کاربری
- بین 3 تا 20 کاراکتر
- فقط حروف، اعداد و underscore

### اعتبارسنجی ایمیل
- فرمت استاندارد ایمیل

### هش کردن رمز عبور
- استفاده از bcrypt با salt

### احراز هویت JWT
- توکن‌های امن با زمان انقضا
- محافظت از مسیرهای حساس

## ساختار پروژه

```
flask-app/
├── app.py              # فایل اصلی اپلیکیشن
├── models.py           # مدل‌های پایگاه داده
├── routes.py           # مسیرهای API
├── run.py              # اسکریپت راه‌اندازی
├── test_simple.py      # تست ساده
├── test_api.py         # تست API
├── requirements.txt    # وابستگی‌ها
├── .env               # متغیرهای محیطی
├── .gitignore         # فایل‌های نادیده گرفته شده
├── README.md          # مستندات کامل
├── SETUP.md           # راهنمای راه‌اندازی
└── templates/
    └── index.html     # رابط کاربری
```

## نکات مهم

### برای محیط تولید (Production)
1. تغییر کلیدهای رمزنگاری در `.env`
2. استفاده از HTTPS
3. تنظیمات امنیتی مناسب
4. استفاده از پایگاه داده تولید (PostgreSQL, MySQL)

### عیب‌یابی
- بررسی لاگ‌های سرور
- تست اتصال پایگاه داده
- بررسی تنظیمات JWT
- اعتبارسنجی متغیرهای محیطی

## پشتیبانی

در صورت بروز مشکل:
1. بررسی فایل‌های لاگ
2. تست اتصال پایگاه داده
3. بررسی تنظیمات محیطی
4. مراجعه به مستندات README.md