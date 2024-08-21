## 1. Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории, произведению может быть присвоен жанр.
Пользователи могут оставлять к произведениям текстовые отзывы и ставить произведению оценку в диапазоне от 1 до 10.
Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
Пользователи могут оставлять комментарии к отзывам.

## 2. Стек проекта (список технологий):

Язык программирования: *Python*
Фреймворк: *Django*
База данных: *SQLite*
API: *Django Rest Framework*
Системы контроля версий: *Git*
Инструменты разработки: *PyCharm, VSCode*
Тестирование: *pytest*
Управление зависимостями: *pip, requirements.txt*

## 3. Как запустить проект: 

Клонировать репозиторий и перейти в него в командной строке 
 
### Cоздать и активировать виртуальное окружение: 

Windows 
``` python -m venv venv ``` 
``` source venv/Scripts/activate ``` 
Linux/macOS 
``` python3 -m venv venv ``` 
``` source venv/bin/activate ``` 

### Обновить PIP 
 
Windows 
``` python -m pip install --upgrade pip ``` 
Linux/macOS 
``` python3 -m pip install --upgrade pip ``` 
 
### Установить зависимости из файла requirements.txt: 
 
``` pip install -r requirements.txt ``` 
 
### Выполнить миграции: 
 
Windows 
``` python manage.py makemigrations ``` 
``` python manage.py migrate ``` 
Linux/macOS 
``` python3 manage.py makemigrations ``` 
``` python3 manage.py migrate ``` 

### Запустить проект: 

Windows 
``` python manage.py runserver ``` 
Linux/macOS 
``` python3 manage.py runserver ``` 

### Загрузить файлы cdv в базу данных:
``` python manage.py import_category ```
``` python manage.py import_comments ```
``` python manage.py import_genre ```
``` python manage.py import_rewiew ```
``` python manage.py import_titlegenre ```
``` python manage.py import_titles ```
``` python manage.py import_users ``` 

## 4. Ссылка на документацию:
[ссылка на документацию](http://127.0.0.1:8000/redoc/)

## 5. Авторы проекта:

Арташкин Евгений
Плахотная Елена 
Эгенбург Ольга 
