# سامانه ثبت‌نام دانشگاه

[![CI](https://github.com/hosseinpv1379/mohammad_mohammadian/actions/workflows/ci.yml/badge.svg)](https://github.com/hosseinpv1379/mohammad_mohammadian/actions/workflows/ci.yml)

<p align="center">
  <img src="https://raw.githubusercontent.com/hosseinpv1379/mohammad_mohammadian/master/docs/screenshots/dashboard.png" alt="داشبورد سامانه ثبت‌نام دانشگاه" width="100%" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/hosseinpv1379/mohammad_mohammadian/master/docs/screenshots/add-course.png" alt="فرم افزودن درس جدید" width="100%" />
</p>

پروژه آزمایشگاه مهندسی نرم‌افزار — REST API ساده برای مدیریت دروس دانشگاه با ذخیره‌سازی در حافظه (بدون دیتابیس).

## زبان و فناوری‌ها

| مورد | انتخاب |
|---|---|
| زبان | **Python 3.11+** |
| فریم‌ورک API | Flask |
| تست | pytest |
| مستندسازی API | Flasgger (Swagger UI + OpenAPI YAML) |
| CI | GitHub Actions |

**چرا Python؟** سینتکس خوانا برای ارائه در کلاس، اکوسیستم تست قوی (pytest)، و پشتیبانی خوب از REST API و Swagger.

## نصب و اجرا

```bash
# کلون مخزن
git clone https://github.com/hosseinpv1379/mohammad_mohammadian.git
cd mohammad_mohammadian

# محیط مجازی (اختیاری ولی توصیه‌شده)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
export PYTHONPATH=src
flask --app university_registration.main:app run --debug
```

سرور روی `http://127.0.0.1:5000` بالا می‌آید.

## رابط کاربری (Frontend)

پس از اجرای سرور، رابط کاربری فارسی را در مرورگر باز کنید:

**http://127.0.0.1:5000**

امکانات UI:
- نمایش لیست دروس با وضعیت ظرفیت
- کارت‌های آماری (تعداد دروس، ظرفیت، ثبت‌نام‌شده)
- مشاهده جزئیات هر درس
- افزودن درس جدید از طریق فرم
- جستجو بر اساس کد یا عنوان

داده‌های نمونه هنگام اولین اجرا به‌صورت خودکار بارگذاری می‌شوند.

## Swagger / OpenAPI

| منبع | آدرس |
|---|---|
| Swagger UI | http://127.0.0.1:5000/docs/ |
| OpenAPI JSON | http://127.0.0.1:5000/apispec.json |
| فایل‌های YAML | `docs/openapi/` |

## Endpoint ها

| Method | Path | توضیح |
|---|---|---|
| `GET` | `/courses` | لیست همه دروس |
| `POST` | `/courses` | افزودن درس جدید |
| `GET` | `/courses/{course_id}` | دریافت درس بر اساس شناسه |
| `GET` | `/health` | بررسی سلامت سرویس |

### نمونه درخواست

```bash
# افزودن درس
curl -X POST http://127.0.0.1:5000/courses \
  -H "Content-Type: application/json" \
  -d '{"id":"cse101","code":"CSE-101","title":"Software Engineering Lab","capacity":40,"professor_id":"prof-1"}'

# لیست دروس
curl http://127.0.0.1:5000/courses

# دریافت یک درس
curl http://127.0.0.1:5000/courses/cse101
```

## اجرای تست‌ها

```bash
pytest -v
```

## ساختار پوشه‌ها

```
.
├── .github/workflows/ci.yml    # GitHub Actions — build & test
├── docs/
│   ├── screenshots/            # اسکرین‌شات‌ها برای README گیت‌هاب
│   ├── class-diagram.puml      # Class Diagram (PlantUML)
│   ├── sequence-diagram.puml   # Sequence Diagram — ثبت‌نام در درس
│   ├── user-stories.md         # User Story ها + Gherkin
│   └── openapi/                # مشخصات Swagger/OpenAPI هر endpoint
├── frontend/                   # رابط کاربری وب (HTML/CSS/JS)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── src/university_registration/
│   ├── api/routes/courses.py   # REST endpoints
│   ├── models/                 # Student, Course, Enrollment, Professor
│   ├── services/               # منطق کسب‌وکار (CourseService)
│   └── main.py                 # نقطه ورود Flask
├── tests/
│   └── test_course_service.py  # Unit tests (AAA pattern)
├── requirements.txt
├── pytest.ini
└── README.md
```

## مدل دامنه (خلاصه)

| کلاس | نقش |
|---|---|
| `Student` | دانشجو و وضعیت بورسیه |
| `Course` | درس، ظرفیت، استاد ارائه‌دهنده |
| `Enrollment` | پیوند دانشجو–درس (وضعیت ثبت‌نام) |
| `Professor` | عضو هیئت علمی و دروس تدریسی |

جزئیات روابط UML در `docs/class-diagram.puml` و سناریوی ثبت‌نام در `docs/sequence-diagram.puml`.

## مجوز

پروژه آموزشی — استفاده آزاد برای ارائه درس.
