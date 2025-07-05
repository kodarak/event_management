# Event Management API

RESTful API для управління подіями, реєстрацією користувачів і відправлення email-повідомлень. Побудовано на Django, Django REST Framework і PostgreSQL із підтримкою JWT-автентифікації, фільтрації подій і email-повідомлень через ukr.net SMTP. Проєкт відповідає всім вимогам тестового завдання, включно з бонусними функціями.

## Реалізований функціонал

- **Модель події (Event)**: модель із полями `title` (назва), `description` (опис), `date` (дата), `location` (локація) та `organizer` (організатор).
- **CRUD операції для подій**: створення, перегляд, оновлення та видалення подій через REST API.
- **Реєстрація та автентифікація користувачів**: реєстрація нових користувачів і автентифікація через JWT-токени.
- **Реєстрація на події**: можливість реєструватися та скасовувати реєстрацію на події.
- **Фільтрація подій** (бонусна функція): пошук і фільтрація подій за назвою, локацією, датою та організатором.
- **Email-повідомлення** (бонусна функція): відправлення HTML-листів із підтвердженням реєстрації на подію через ukr.net SMTP.
- **Документація API**: опис усіх ендпоінтів і прикладів запитів у цьому README-файлі.
- **Docker**: проєкт упаковано в Docker-контейнери з PostgreSQL для легкого розгортання.

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

5. **Побудуйте та запустіть проєкт**:

   ```cmd
   docker-compose up --build
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

1. **Реєстрація користувача** (POST):

   ```cmd
   curl -H "Content-Type: application/json" -X POST http://localhost:8000/api/register/ -d "{\"username\":\"testuser\",\"password\":\"testpass123\",\"email\":\"testuser@ukr.net\"}"
   ```

2. **Отримання JWT-токена** (POST):

   ```cmd
   curl -X POST http://localhost:8000/api/token/ -d "username=root&password=maga123!@#"
   ```
   
3. **Перегляд списку подій** (GET з фільтрацією):

   ```cmd
   curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/?title=Test
   ```
   
4. **Створення події** (POST):

   ```cmd
   curl -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -X POST http://localhost:8000/api/events/ -d "{\"title\":\"Test Event\",\"description\":\"Test description\",\"date\":\"2025-07-30T15:00:00Z\",\"location\":\"Kyiv\"}"
   ```

5. **Перегляд деталів події** (GET):

   ```cmd
   curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/1/
   ```

6. **Оновлення події** (PUT):

   ```cmd
   curl -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -X PUT http://localhost:8000/api/events/1/ -d "{\"title\":\"Updated Event\",\"description\":\"Updated description\",\"date\":\"2025-07-30T15:00:00Z\",\"location\":\"Kyiv\"}"
   ```

7. **Видалення події** (DELETE):

   ```cmd
   curl -H "Authorization: Bearer <access_token>" -X DELETE http://localhost:8000/api/events/1/
   ```
   
8. **Реєстрація на подію** (POST, відправляє email):
   ```cmd
   curl -H "Authorization: Bearer <access_token>" -X POST http://localhost:8000/api/events/1/register/
   ```
   ![image](https://github.com/user-attachments/assets/4772ef6a-f5da-4c34-a8e2-8bca3ff3eabe)
