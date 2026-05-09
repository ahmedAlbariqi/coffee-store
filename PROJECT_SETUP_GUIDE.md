# Django Project Setup Guide
# دليل إنشاء مشروع Django من الصفر

---

## المرحلة الأولى: إعداد البيئة
1. إنشاء مجلد المشروع
   mkdir project_name
   cd project_name

2. إنشاء البيئة الافتراضية وتفعيلها
   python -m venv venv
   .\venv\Scripts\activate

3. تثبيت المكتبات الأساسية
   pip install django django-environ pillow

4. حفظ المكتبات
   pip freeze > requirements.txt

---

## المرحلة الثانية: إنشاء المشروع والهيكل
5. إنشاء مشروع Django
   django-admin startproject config .

6. إنشاء مجلد التطبيقات
   mkdir apps

7. إنشاء التطبيقات داخل apps
   cd apps
   django-admin startapp app_name
   cd ..

8. إنشاء المجلدات الأساسية
   mkdir templates
   mkdir static
   mkdir media

9. إنشاء ملفات البيئة
   New-Item .env
   New-Item .gitignore
   New-Item CLAUDE.md
   New-Item COMMANDS.md

---

## المرحلة الثالثة: الإعدادات ⚠️ مرتبة بدقة
10. إعداد ملف .env بالقيم الأساسية

11. إعداد settings.py بالترتيب التالي:
    أ. ربط django-environ
    ب. إضافة التطبيقات في INSTALLED_APPS
    ج. ⚠️ تحديد AUTH_USER_MODEL إذا كان لديك CustomUser
       AUTH_USER_MODEL = 'accounts.CustomUser'
    د. إعداد TEMPLATES, STATIC, MEDIA
    هـ. إعداد LANGUAGE_CODE و TIME_ZONE

12. تصحيح apps.py في كل تطبيق
    name = 'apps.app_name'  ← وليس name = 'app_name'

---

## المرحلة الرابعة: قاعدة البيانات ⚠️ بعد الإعدادات مباشرة
13. إنشاء CustomUser model أولاً إذا احتجته

14. ⚠️ makemigrations قبل migrate
    python manage.py makemigrations
    python manage.py migrate

15. إنشاء حساب Admin
    python manage.py createsuperuser

---

## المرحلة الخامسة: التحقق
16. تشغيل السيرفر والتأكد من عمله
    python manage.py runserver
    http://127.0.0.1:8000
    http://127.0.0.1:8000/admin

---

## ⚠️ تحذيرات مهمة لا تنساها
- دائماً فعّل البيئة الافتراضية أول شيء
- حدد AUTH_USER_MODEL قبل أي migrate
- صحح apps.py بعد كل startapp جديد
- لا ترفع .env على GitHub أبداً
- makemigrations ثم migrate دائماً بهذا الترتيب