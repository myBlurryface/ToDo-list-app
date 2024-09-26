# Использование базового образа Python
FROM python:3.12-slim

# Установка зависимостей для компиляции пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочую директорию
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Устанавливака зависимостей
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование всех файлов проекта
COPY . .

# Открытие рабочего порта для работы
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

