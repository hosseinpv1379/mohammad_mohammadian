# اسکرین‌شات‌های پروژه

این پوشه را برای README گیت‌هاب استفاده کنید.

## پیشنهاد اسکرین‌شات‌ها

1. `dashboard.png` — صفحه اصلی با لیست دروس و کارت‌های آماری
2. `course-detail.png` — انتخاب یک درس و نمایش جزئیات سمت راست
3. `add-course.png` — مودال افزودن درس جدید
4. `swagger.png` — صفحه Swagger در `/docs/`

## نحوه گرفتن اسکرین‌شات

```bash
export PYTHONPATH=src
flask --app university_registration.main:app run --debug
```

سپس در مرورگر باز کنید: http://127.0.0.1:5000

بعد از گرفتن عکس‌ها، آن‌ها را اینجا قرار دهید و در README لینک دهید:

```markdown
![داشبورد](docs/screenshots/dashboard.png)
```
