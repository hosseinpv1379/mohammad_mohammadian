# User Stories — سامانه ثبت‌نام دانشگاه

## Story 1 — محدودیت ظرفیت بخش درسی

**As a** department head  
**I want** each course section to reject registration once classroom capacity is reached  
**So that** students are not assigned to physically overcrowded rooms during peak registration week.

| معیار INVEST | ارزیابی | توضیح |
|---|---|---|
| **I**ndependent | ✅ | قابل پیاده‌سازی با مدل `Course.capacity` و شمارش `Enrollment` بدون وابستگی به ماژول‌های دیگر |
| **N**egotiable | ✅ | می‌توان ظرفیت را ثابت یا پویا (بر اساس سالن) در نظر گرفت |
| **V**aluable | ✅ | جلوگیری از مشکل عملیاتی و شکایت دانشجویان |
| **E**stimable | ✅ | تخمین ۱–۲ روز کاری برای لایه سرویس و تست |
| **S**mall | ✅ | یک قانیل کسب‌وکار مشخص: «ظرفیت پر = رد ثبت‌نام» |
| **T**estable | ✅ | با mock کردن تعداد ثبت‌نام‌ها قابل تست است |

---

## Story 2 — معافیت شهریه بورسیه‌ای هنگام ثبت‌نام

**As a** scholarship student  
**I want** my tuition waiver to be applied automatically when I enroll in a course  
**So that** I do not need a separate visit to the finance office for each semester.

| معیار INVEST | ارزیابی | توضیح |
|---|---|---|
| **I**ndependent | ✅ | فقط به فیلد `Student.scholarship` و `Enrollment.tuitionWaived` نیاز دارد |
| **N**egotiable | ✅ | می‌توان درصد معافیت یا سقف واحد را بعداً اضافه کرد |
| **V**aluable | ✅ | کاهش بار اداری و خطای انسانی |
| **E**stimable | ✅ | منطق شرطی ساده؛ تخمین کمتر از یک اسپرینت |
| **S**mall | ✅ | یک رویداد در جریان ثبت‌نام |
| **T**estable | ✅ | دو سناریو: بورسیه / غیربورسیه |

---

## Story 3 — نمایش تعداد لیست انتظار برای استاد

**As a** professor  
**I want** to see the waitlist count for my course before the semester starts  
**So that** I can request a larger classroom if demand exceeds capacity.

| معیار INVEST | ارزیابی | توضیح |
|---|---|---|
| **I**ndependent | ✅ | فقط خواندن وضعیت ثبت‌نام و لیست انتظار |
| **N**egotiable | ✅ | می‌توان آستانه هشدار (مثلاً ۱۰٪ بیش از ظرفیت) تعریف کرد |
| **V**aluable | ✅ | تصمیم‌گیری بهتر برای تخصیص منابع فیزیکی |
| **E**stimable | ✅ | یک endpoint گزارش‌گیری ساده |
| **S**mall | ✅ | فقط query روی Enrollment با status=waitlisted |
| **T**estable | ✅ | با داده‌های از پیش seed شده قابل تأیید است |

---

## Acceptance Criteria (Gherkin) — Story 1: محدودیت ظرفیت

### مسیر موفق

```gherkin
Feature: Course capacity enforcement

  Scenario: Student enrolls when seats are available
    Given course "CSE-101" has capacity 40 and 39 active enrollments
    And student "S-1001" is eligible for registration
    When the student submits enrollment for "CSE-101"
    Then the enrollment status should be "active"
    And the course active enrollment count should be 40
```

### مسیر خطا

```gherkin
  Scenario: Student is rejected when course is full
    Given course "CSE-101" has capacity 40 and 40 active enrollments
    And student "S-1002" is eligible for registration
    When the student submits enrollment for "CSE-101"
    Then the system should return error "capacity exceeded"
    And no new enrollment record should be created
```
