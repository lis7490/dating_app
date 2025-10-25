FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создайте папки для медиа файлов
RUN mkdir -p /app/media /app/staticfiles

# Дайте права на запись
RUN chmod -R 755 /app/media

# Соберите статические файлы
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]