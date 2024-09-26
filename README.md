```markdown
# **Todo List API app**

Это REST API для управления задачами с использованием Django и PostgreSQL. Проект поддерживает аутентификацию с использованием JWT и использует Docker для контейнеризации приложения.

## Основные возможности

- Регистрация и аутентификация пользователей
- Создание, обновление и удаление задач
- Фильтрация задач по статусу и пользователям
- Маркировка задач как выполненных
- Поддержка аутентификации JWT

## Стек технологий

- Python 3.12
- Django Rest Framework
- PostgreSQL
- Docker и Docker Compose
- JWT для аутентификации

## Требования

Для запуска проекта вам потребуется:

- Docker и Docker Compose
- Python 3.12 (если не использовать Docker)
- Установленная и настроенная база данных PostgreSQL
```

## Установка

### Шаг 1: Установка и настройка PostgreSQL

#### 1. Установка PostgreSQL

##### macOS (с Homebrew):
```bash
brew install postgresql
brew services start postgresql
```

##### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

##### Linux (Fedora/RHEL):
```bash
sudo dnf install postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl start postgresql
```

##### Windows:
Загрузите и установите PostgreSQL: [PostgreSQL для Windows](https://www.postgresql.org/download/windows/)

#### 2. Настройка PostgreSQL

1. Войдите в PostgreSQL как суперпользователь:
   ```bash
   sudo -u postgres psql
   ```

2. Создайте пользователя и базу данных:
   ```sql
   CREATE USER todo_user WITH PASSWORD 'todo_password';
   CREATE DATABASE todo_db;
   GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;
   \q
   ```

### Шаг 2: Клонирование репозитория

Склонируйте репозиторий на вашу локальную машину:

```bash
git clone https://github.com/myBlurryface/ToDo-list-app.git
cd ToDo-list-app
```

### Шаг 3: Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта. Пример содержимого:

```bash
DB_NAME=todo_db # Название базы данных
DB_USER=todo_user # Имя пользователя PostgreSQL 
DB_PASSWORD=todo_password # Пароль пользователя PostgreSQL
DB_HOST=localhost # Хост, если не использовать Docker 
DB_PORT=5432 # Порт подключения 

# Если используете Docker, то настройте еще эти переменные оружения
POSTGRES_DB=todo_db # Совпадает с DB_NAME
POSTGRES_USER=todo_user # Совпадает с DB_USER
POSTGRES_PASSWORD=todo_password # Совпадает с DB_PASSWORD
DB_HOST=db # Будет принимать значения db в случае использования Docker
```

### Шаг 4: Запуск с использованием Docker

1. Перейдите в корневую директорию проекта. Затем постройте и запустите контейнеры:

    ```bash
    docker compose up --build
    ```

2. Выполните миграции базы данных:

    ```bash
    docker compose exec web python manage.py migrate
    ```

3. Создайте суперпользователя для доступа к Django admin:

    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

Теперь приложение доступно по адресу `http://localhost:8000`.

### Шаг 5: Локальный запуск (без Docker)

Если вы хотите запустить проект без Docker:

1. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

2. Выполните миграции базы данных:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

4. Создайте суперпользователя:

    ```bash
    python manage.py createsuperuser
    ```
### **Models Overview**

#### **User Model**

Модель пользователя является кастомной и наследуется от `AbstractUser`.

**Основные поля:**
- **first_name**: имя пользователя (обязательно). # max_length = 50
- **last_name**: фамилия пользователя (опционально). # max_length = 50
- **username**: уникальное имя пользователя (обязательно). # max_length = 20
- **password**: пароль, минимальная длина контролируется валидацией. # max_length = 128

#### **Task Model**

Модель задач связана с моделью пользователя через внешний ключ.

**Основные поля:**
- **title**: заголовок задачи (обязательно). # max_length = 80
- **description**: описание задачи (опционально). # max_length = 140
- **status**: статус задачи с выбором (`new`, `in_progress`, `completed`), по умолчанию — `new`. # max_length = 20
- **user**: связь с моделью пользователя (ForeignKey, удаление задачи при удалении пользователя).

## API Документация

### Аутентификация

- Получение JWT токенов:
  - URL: `/api/api/token/`
  - Метод: `POST`
  - Параметры:
    ```json
    {
      "username": "ваш_username",
      "password": "ваш_пароль"
    }
    ```

- Обновление JWT токена:
  - URL: `/api/api/token/refresh/`
  - Метод: `POST`
  - Параметры:
    ```json
    {
      "refresh": "ваш_refresh_token"
    }
    ```

### Задачи (Tasks)

- Получение всех задач:
  - URL: `/api/tasks/`
  - Метод: `GET`
  - Аутентификация: требуется

- Получение задач пользователя:
  - URL: `/api/tasks/user/<username>/`
  - Метод: `GET`
  - Аутентификация: требуется

- Создание новой задачи (новая задача присваевается пользователю, отправившему запрос):
  - URL: `/api/tasks/create/`
  - Метод: `POST`
  - Аутентификация: требуется
  - Параметры:
    ```json
    {
      "title": "Название задачи",
      "description": "Описание задачи",
      "status": "new"
    }
    ```

- Получение информации о задаче:
  - URL: `/api/tasks/<id>/`
  - Метод: `GET`
  - Аутентификация: требуется

- Обновление задачи:
  - URL: `/api/tasks/<id>/update/`
  - Метод: `PATCH`
  - Аутентификация: требуется (только владелец может обновлять задачу)
  - Параметры:
    ```json
    {
      "title": "Обновленное название задачи",
      "description": "Обновленное описание задачи",
      "status": "in_progress"
    }
    ```

- Удаление задачи:
  - URL: `/api/tasks/<id>/delete/`
  - Метод: `DELETE`
  - Аутентификация: требуется (только владелец может удалять задачу)

- Фильтрация задач по статусу:
  - URL: `/api/tasks/status/<status>/`
  - Метод: `GET`
  - Аутентификация: требуется

- Маркировка задачи как выполненной:
  - URL: `/api/tasks/<id>/complete/`
  - Метод: `PATCH`
  - Аутентификация: требуется

##### **Pagination**

Все API-эндпоинты, возвращающие списки задач, используют по умолчанию пагинацию. В данном проекте каждая страница содержит в себе до 10 задач.

- Параметр `page`: используется для указания номера страницы.
  
Пример использования:

```bash
GET /api/tasks/?page=2
```

Пример ответа:

```json
{
    "count": 25,
    "next": "http://example.com/api/tasks/?page=3",
    "previous": "http://example.com/api/tasks/?page=1",
    "results": [
        {
            "id": 11,
            "title": "Task title",
            "description": "Task description",
            "status": "new",
            "user": 1
        },
        ...
    ]
}
```

- **count**: общее количество объектов.
- **next**: ссылка на следующую страницу (если она есть).
- **previous**: ссылка на предыдущую страницу (если она есть).
- **results**: список задач на текущей странице.

## Добавление пользователей для ручного тестирования через Django Admin

Панель администратора доступна по адресу:

```
http://localhost:8000/admin/
```

Здесь можно добавить пользователей для ручного тестирования.

## Автоматическое тестирование

Запуск тестов:

```bash
# Используя Docker
docker compose exec web python manage.py test
# Не используя Docker
python manage.py test
```

## Автор

- Лозицкий Константин — ralf_201@hotmail.com
- GitHub: [ваш GitHub профиль](https://github.com/myBlurryface)