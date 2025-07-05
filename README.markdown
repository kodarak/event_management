# Event Management API

RESTful API для управління подіями, реєстрацією користувачів і відправлення email-повідомлень. Побудовано на Django, Django REST Framework і PostgreSQL із підтримкою JWT-автентифікації, фільтрації подій і email-повідомлень через ukr.net.

## Особливості

- **Керування користувачами**: реєстрація та автентифікація через JWT-токени.
- **Керування подіями**: створення, перегляд, оновлення, видалення подій (CRUD).
- **Реєстрація на події**: реєстрація та скасування реєстрації на події.
- **Фільтрація подій**: пошук подій за назвою, локацією, діапазоном дат і організатором.
- **Email-повідомлення**: відправлення HTML-листів із підтвердженням реєстрації через ukr.net SMTP.
- **Docker**: запуск у контейнерах через Docker Compose.

## Технології

- Python 3.8+
- Django 3.2
- Django REST Framework 3.12.4
- PostgreSQL
- django-filter 21.1
- djangorestframework-simplejwt 5.2.0
- gunicorn 21.2.0
- python-decouple 3.5
- ukr.net SMTP для email-повідомлень

## Вимоги

- Docker і Docker Compose
- Обліковий запис ukr.net із паролем для програм (App Password)
- Git (для клонування репозиторію)

## Встановлення

1. **Встановіть Docker**:

   - Завантажте та встановіть Docker Desktop для Windows: https://www.docker.com/products/docker-desktop/
   - Перевірте встановлення:
     ```cmd
     docker --version
     docker-compose --version
     ```

2. **Клонуйте репозиторій**:

   ```cmd
   git clone <repository-url>
   cd event_management
   ```

3. **Створіть `.env` файл**:
   У корені проєкту створіть файл `.env`:

   ```cmd
   echo SECRET_KEY=your-very-long-random-secret-key-1234567890abcdef> .env
   echo DEBUG=True>> .env
   echo DB_NAME=event_management>> .env
   echo DB_USER=user>> .env
   echo DB_PASSWORD=password>> .env
   echo DB_HOST=db>> .env
   echo DB_PORT=5432>> .env
   echo EMAIL_HOST_USER=your-email@ukr.net>> .env
   echo EMAIL_HOST_PASSWORD=your-app-password>> .env
   echo DJANGO_SUPERUSER_PASSWORD=maga123!@#>> .env
   ```

   - Замініть `your-very-long-random-secret-key-1234567890abcdef` на унікальний ключ (згенеруйте: https://djecrety.ir/).
   - Замініть `your-email@ukr.net` на вашу email-адресу ukr.net.
   - Замініть `your-app-password` на пароль для програм (див. Налаштування ukr.net).

4. **Налаштуйте ukr.net SMTP**:

   - Увійдіть на `https://mail.ukr.net`.
   - Перейдіть до **Налаштування > Налаштування IMAP/SMTP**.
   - Увімкніть **Доступ через IMAP/SMTP**.
   - Створіть **Пароль для програм** у розділі **Паролі для зовнішніх програм**.
   - Оновіть `.env` із цими значеннями.

5. **Створіть директорію для шаблонів**:

   ```cmd
   mkdir templates\email
   echo. > templates\email\event_registration.html
   ```

   Додайте наступний вміст до `templates\email\event_registration.html`:

   ```html
   <!DOCTYPE html>
   <html>
     <head>
       <meta charset="UTF-8" />
       <title>Підтвердження реєстрації на подію</title>
     </head>
     <body
       style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;"
     >
       <div
         style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;"
       >
         <h2 style="color: #2c3e50;">Підтвердження реєстрації на подію</h2>
         <p>Шановний {{ user.username }},</p>
         <p>Ви успішно зареєструвалися на подію:</p>
         <h3 style="color: #2980b9;">{{ event.title }}</h3>
         <p><strong>Дата:</strong> {{ event.date }}</p>
         <p><strong>Локація:</strong> {{ event.location }}</p>
         <p><strong>Опис:</strong> {{ event.description }}</p>
         <p>Чекаємо вас на події!</p>
         <p style="margin-top: 20px;">
           З найкращими побажаннями,<br />Команда Event Management
         </p>
       </div>
     </body>
   </html>
   ```

6. **Побудуйте та запустіть проєкт**:

   ```cmd
   docker-compose up --build
   ```

7. **Застосуйте міграції**:
   ```cmd
   docker-compose exec web python manage.py migrate
   ```

## Запуск проєкту

1. Запустіть контейнери:
   ```cmd
   docker-compose up
   ```
2. API доступне за адресою `http://localhost:8000`.

## Документація API

API підтримує наступні ендпоінти для управління подіями та користувачами. Усі захищені ендпоінти потребують JWT-токен, який можна отримати через `/api/token/`.

| Ендпоінт                       | Метод  | Опис                              | Автентифікація |
| ------------------------------ | ------ | --------------------------------- | -------------- |
| `/api/register/`               | POST   | Реєстрація нового користувача     | Немає          |
| `/api/token/`                  | POST   | Отримання JWT-токена              | Немає          |
| `/api/token/refresh/`          | POST   | Оновлення JWT-токена              | Немає          |
| `/api/events/`                 | GET    | Список усіх подій (з фільтрацією) | JWT            |
| `/api/events/`                 | POST   | Створення нової події             | JWT            |
| `/api/events/<id>/`            | GET    | Деталі події                      | JWT            |
| `/api/events/<id>/`            | PUT    | Оновлення події                   | JWT            |
| `/api/events/<id>/`            | DELETE | Видалення події                   | JWT            |
| `/api/events/<id>/register/`   | POST   | Реєстрація на подію               | JWT            |
| `/api/events/<id>/unregister/` | POST   | Скасування реєстрації на подію    | JWT            |

### Фільтрація подій

Ендпоінт `/api/events/` підтримує фільтрацію за наступними параметрами:

- `title`: Частковий збіг назви події (наприклад, `?title=Tech`).
- `location`: Частковий збіг локації (наприклад, `?location=Kyiv`).
- `date`: Точна дата (наприклад, `?date=2025-07-30T15:00:00Z`).
- `date__gte`: Дата після (наприклад, `?date__gte=2025-07-01T00:00:00Z`).
- `date__lte`: Дата до (наприклад, `?date__lte=2025-07-31T23:59:59Z`).
- `organizer`: ID організатора (наприклад, `?organizer=1`).

### Приклади запитів

1. **Реєстрація користувача**:

   ```cmd
   curl -H "Content-Type: application/json" -X POST http://localhost:8000/api/register/ -d "{\"username\":\"testuser\",\"password\":\"testpass123\",\"email\":\"testuser@ukr.net\"}"
   ```

2. **Отримання JWT-токена**:

   ```cmd
   curl -X POST http://localhost:8000/api/token/ -d "username=root&password=maga123!@#"
   ```

3. **Створення події**:

   ```cmd
   curl -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -X POST http://localhost:8000/api/events/ -d "{\"title\":\"Test Event\",\"description\":\"Test description\",\"date\":\"2025-07-30T15:00:00Z\",\"location\":\"Kyiv\"}"
   ```

4. **Фільтрація подій**:

   ```cmd
   curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/?title=Test
   curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/?date__gte=2025-07-01T00:00:00Z&date__lte=2025-07-31T23:59:59Z
   ```

5. **Реєстрація на подію** (відправляє email):
   ```cmd
   curl -H "Authorization: Bearer <access_token>" -X POST http://localhost:8000/api/events/1/register/
   ```
