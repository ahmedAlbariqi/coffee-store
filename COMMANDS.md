# Coffee Store - Project Commands
# مشروع متجر القهوة - دليل الأوامر

## 1. Activate Virtual Environment | تفعيل البيئة الافتراضية
.\venv\Scripts\activate

## 2. Run Development Server | تشغيل السيرفر المحلي
python manage.py runserver

## 3. Database Commands | أوامر قاعدة البيانات
# إنشاء ملفات الترحيل بعد تعديل الموديلز
python manage.py makemigrations
# تطبيق التغييرات على قاعدة البيانات
python manage.py migrate

## 4. Create Superuser | إنشاء مستخدم Admin
python manage.py createsuperuser

## 5. Change Superuser Password | تغيير كلمة مرور Admin
python manage.py changepassword admin

## 6. Install Requirements | تثبيت المكتبات
pip install -r requirements.txt

## 7. Update Requirements File | تحديث ملف المكتبات
pip freeze > requirements.txt

## Admin Panel | لوحة التحكم
http://127.0.0.1:8000/admin