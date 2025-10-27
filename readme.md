
# LoveFinder 🔥

**Gлатформа для поиска стратегических отношений**

![LoveFinder](https://img.shields.io/badge/Version-1.0.0-red)
![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

О проекте

LoveFinder — это не очередное приложение для знакомств. Это **тактическая платформа** для сильных личностей, готовых к настоящим отношениям без компромиссов. 

Система использует передовые алгоритмы для поиска идеальных партнеров на основе совместимости характеров, целей и ценностей.

## Особенности

### Брутальный дизайн
- **Военная эстетика** с темной цветовой схемой
- **Техно-стиль** с элементами глитча и анимациями
- **Тактическая терминология** во всем интерфейсе
- **Адаптивный дизайн** для всех устройств

### Ключевые возможности
- **Умный подбор** партнеров на основе алгоритмов совместимости
- **Безопасное общение** с шифрованием данных
- **Тактический поиск** с продвинутыми фильтрами
- **Боевая статистика** активности профиля
- **Стратегические мэтчи** с детальной аналитикой

### Безопасность
- **JWT аутентификация**
- **Военное шифрование** данных
- **Защита от ботов** и фейковых профилей
- **Контроль приватности**

## Быстрый старт

### Предварительные требования
- Docker & Docker Compose
- Python 3.9+
- Node.js (для статических файлов)

### Установка и запуск

1. **Клонирование репозитория**
```bash
git clone https://github.com/lis7490/dating_app.git

Настройка окружения


Запуск через Docker

bash
docker-compose up --build
Миграции и статические файлы

bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
Создание суперпользователя

bash
docker-compose exec web python manage.py createsuperuser
Приложение будет доступно по адресу: http://localhost:8000

📁 Структура проекта
text
lovefinder/
├── dating_project/          # Настройки Django проекта
│   ├── settings.py         # Конфигурация
│   ├── urls.py            # Главные URL patterns
│   └── wsgi.py            # WSGI конфигурация
├── users/                  # Приложение пользователей
│   ├── models.py          # Модели User, Profile, Photo
│   ├── views.py           # API views
│   ├── views_pages.py     # HTML views
│   └── urls.py            # URL routing
├── interactions/          # Приложение взаимодействий
│   ├── models.py          # Модели лайков, мэтчей
│   ├── views.py           # API views для взаимодействий
│   └── urls.py            # URL routing
├── templates/             # HTML шаблоны
│   ├── base.html          # Базовый шаблон
│   ├── home.html          # Главная страница
│   ├── profile.html       # Профиль пользователя
│   └── ...               # Другие страницы
├── media/                 # Медиа файлы
├── static/               # Статические файлы
├── docker-compose.yml    # Docker композ
├── Dockerfile           # Docker образ
└── requirements.txt     # Зависимости Python
Использование
Demo аккаунты
Для тестирования доступны демо-аккаунты:

Аккаунт 1:

Email: user1@demo.com

Пароль: demo123

Аккаунт 2:

Email: user2@demo.com

Пароль: demo123

Основные страницы
/ - Тактическая главная страница

/login/ - Аутентификация

/register/ - Регистрация нового пользователя

/dashboard/ - Командный центр

/profile/ - База профиля

/discover/ - Поиск целей

/matches/ - Активные контакты

/history/ - Архив операций

Технологии
Backend
Django 4.2 - основной фреймворк

Django REST Framework - API

Simple JWT - аутентификация

PostgreSQL - база данных

Redis - кэширование

Frontend
Bootstrap 5 - UI фреймворк

Vanilla JavaScript - клиентская логика

Font Awesome - иконки

Custom CSS - брутальный дизайн

Инфраструктура
Docker - контейнеризация

Nginx - веб-сервер

Gunicorn - WSGI сервер

API Endpoints
Аутентификация
POST /api/token/ - Получить JWT токен

POST /api/token/refresh/ - Обновить токен

POST /api/token/verify/ - Проверить токен

Пользователи
GET /api/users/profiles/me/ - Мой профиль

PUT /api/users/profiles/me/ - Обновить профиль

GET /api/users/photos/ - Мои фото

POST /api/users/photos/ - Загрузить фото

Взаимодействия
GET /api/interactions/likes/ - Лайки

POST /api/interactions/likes/ - Поставить лайк

GET /api/interactions/matches/ - Мэтчи

GET /api/interactions/discover/ - Поиск пользователей

Разработка
Локальная разработка
bash
# Установка зависимостей
pip install -r requirements.txt

# Миграции
python manage.py migrate

# Запуск сервера
python manage.py runserver
Тестирование
bash
python manage.py test
Линтинг
bash
flake8 .
black .
Производительность
Оптимизированные запросы к базе данных

Кэширование часто используемых данных

Асинхронные задачи для тяжелых операций

CDN для статических файлов

Безопасность
HTTPS принудительно в продакшене

CORS настройки

CSRF защита

XSS защита

SQL injection protection

Rate limiting для API





