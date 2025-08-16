# Flask Application API

یک اپلیکیشن Flask امن و ماژولار با احراز هویت JWT و مدیریت کاربران.

## ویژگی‌ها

- ✅ احراز هویت JWT
- ✅ هش کردن رمز عبور با bcrypt
- ✅ اعتبارسنجی ورودی‌ها
- ✅ مدیریت کاربران
- ✅ ساختار ماژولار
- ✅ مستندات کامل API

## نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- pip

### مراحل نصب

1. **کلون کردن پروژه:**
```bash
git clone <repository-url>
cd flask-app
```

2. **نصب وابستگی‌ها:**
```bash
pip install -r requirements.txt
```

3. **تنظیم متغیرهای محیطی:**
فایل `.env` را ویرایش کنید:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
```

4. **اجرای سرور:**
```bash
python app.py
```

سرور روی `http://localhost:5000` اجرا می‌شود.

## API Endpoints

### احراز هویت

#### ثبت نام کاربر جدید
```http
POST /auth/register
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "first_name": "نام",
    "last_name": "نام خانوادگی"
}
```

#### ورود کاربر
```http
POST /auth/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "SecurePass123"
}
```

یا با ایمیل:
```http
POST /auth/login
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "SecurePass123"
}
```

#### دریافت پروفایل کاربر
```http
GET /auth/profile
Authorization: Bearer <jwt_token>
```

### مدیریت کاربران

#### دریافت همه کاربران
```http
GET /users/
Authorization: Bearer <jwt_token>
```

#### دریافت کاربر خاص
```http
GET /users/{user_id}
Authorization: Bearer <jwt_token>
```

#### به‌روزرسانی پروفایل
```http
PUT /users/{user_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "first_name": "نام جدید",
    "last_name": "نام خانوادگی جدید",
    "email": "newemail@example.com"
}
```

#### حذف حساب کاربری
```http
DELETE /users/{user_id}
Authorization: Bearer <jwt_token>
```

### سایر Endpoints

#### صفحه اصلی
```http
GET /
```

#### بررسی وضعیت سرور
```http
GET /health
```

## کدهای وضعیت HTTP

- `200` - موفقیت
- `201` - ایجاد شده
- `400` - درخواست نامعتبر
- `401` - عدم احراز هویت
- `403` - عدم دسترسی
- `404` - یافت نشد
- `409` - تداخل
- `500` - خطای سرور

## نکات امنیتی

### تولید (Production)

1. **تغییر کلیدهای رمزنگاری:**
   - `SECRET_KEY` را تغییر دهید
   - `JWT_SECRET_KEY` را تغییر دهید

2. **استفاده از HTTPS:**
   - در محیط تولید حتماً از HTTPS استفاده کنید
   - تنظیمات SSL/TLS مناسب اعمال کنید

3. **تنظیمات JWT:**
   - زمان انقضای توکن را تنظیم کنید
   - از کلیدهای قوی استفاده کنید

4. **اعتبارسنجی ورودی:**
   - تمام ورودی‌های کاربر اعتبارسنجی می‌شوند
   - از SQL Injection محافظت شده است

### اعتبارسنجی رمز عبور

رمز عبور باید شامل موارد زیر باشد:
- حداقل 8 کاراکتر
- حداقل یک حرف بزرگ
- حداقل یک حرف کوچک
- حداقل یک عدد

### اعتبارسنجی نام کاربری

نام کاربری باید:
- بین 3 تا 20 کاراکتر باشد
- فقط شامل حروف، اعداد و underscore باشد

## ساختار پروژه

```
flask-app/
├── app.py              # فایل اصلی اپلیکیشن
├── models.py           # مدل‌های پایگاه داده
├── routes.py           # مسیرهای API
├── requirements.txt    # وابستگی‌ها
├── .env               # متغیرهای محیطی
├── README.md          # مستندات
└── app.db             # پایگاه داده SQLite
```

## تست API

### با curl

#### ثبت نام:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "first_name": "نام",
    "last_name": "نام خانوادگی"
  }'
```

#### ورود:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123"
  }'
```

#### دریافت پروفایل:
```bash
curl -X GET http://localhost:5000/auth/profile \
  -H "Authorization: Bearer <your_jwt_token>"
```

### با Postman

1. فایل‌های JSON نمونه را در پوشه `examples/` مشاهده کنید
2. درخواست‌ها را در Postman وارد کنید
3. توکن JWT را در header `Authorization` قرار دهید

## عیب‌یابی

### مشکلات رایج

1. **خطای Import:**
   - مطمئن شوید که تمام وابستگی‌ها نصب شده‌اند
   - از محیط مجازی استفاده کنید

2. **خطای پایگاه داده:**
   - فایل `app.db` را حذف کنید و دوباره اجرا کنید
   - مطمئن شوید که مسیر پایگاه داده درست است

3. **خطای JWT:**
   - کلیدهای JWT را بررسی کنید
   - زمان انقضای توکن را تنظیم کنید

## مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید
3. تغییرات را commit کنید
4. Pull Request ارسال کنید

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.