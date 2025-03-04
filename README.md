
# **RESTful API сервис для реферальной системы**

## Описание

Этот сервис реализует функционал реферальной системы, где пользователи могут регистрироваться, создавать реферальные коды, приглашать других пользователей и получать информацию о своих рефералах. Сервис поддерживает регистрацию и авторизацию с использованием JSON Web Tokens (JWT), что обеспечивает безопасность и защиту данных.

## Функциональные возможности

- **Регистрация и аутентификация пользователя**: регистрация пользователей с использованием JSON Web Tokens (JWT).
- **Создание и управление реферальными кодами**: аутентифицированный пользователь может создать один реферальный код, задать срок его действия и удалить его при необходимости.
- **Получение реферального кода**: возможность получить реферальный код пользователя по email реферера.
- **Регистрация по реферальному коду**: регистрация новых пользователей в качестве рефералов через реферальный код.
- **Получение информации о рефералах**: пользователи могут получать информацию о своих рефералах по их ID.

## Дополнительно реализовано

- **Проверка email**: интеграция с [emailhunter.co](https://emailhunter.co) для проверки корректности указанных email-адресов.
- **Кэширование реферальных кодов**: для ускорения работы используется Redis для хранения данных о реферальных кодах.

## Стек технологий

Сервис написан на **Python** с использованием следующих библиотек и фреймворков:
- **FastAPI** - основной фреймворк для создания API
- **FastAPI-Users** - управление пользователями и их авторизацией
- **Uvicorn** - ASGI сервер для запуска приложения
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация данных
- **Redis** - кэширование данных о реферальных кодах

## Конфигурация

Для работы приложения необходимо создать файл `.env`, скопировав пример из `.env.example`, и заполнить необходимые данные (например, переменные для подключения к базе данных и Redis, ключи для emailhunter.co и другие настройки).

## Установка и запуск

1. **Провести миграции** в базу данных:
   ```bash
   alembic upgrade head
   ```

2. **Запустить приложение**:
   ```bash
   uvicorn src.main:app --reload
   ```

**Запуск с использованием Docker**:
   Вы можете также запустить приложение в контейнере Docker:
   ```bash
   docker-compose up --build
   ```
