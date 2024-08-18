from users.models import User   
from reviews.models import (
    Title, Category, Genre, TitleGenre,
    Comments, Reviews)
import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()


def import_users_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        # Используем DictReader для работы с заголовками
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            user, created = User.objects.get_or_create(
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            if created:
                print(f"Создан пользователь: {user.username}")
            else:
                print(f"Пользователь уже существует: {user.username}")


def import_titles_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            title, created = Title.objects.get_or_create(
                name=row['name'],
                year=row['year'],
                category=row['category'],
            )
            if created:
                print(f"Создано произведение: {title.name}")
            else:
                print(f"Произведение уже существует: {title.name}")


def import_categories_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            category, created = Category.objects.get_or_create(
                name=row['name'],
                slug=row['slug']
            )
            if created:
                print(f"Создана категория: {category.name}")
            else:
                print(f"Категория уже существует: {category.name}")

def import_comments_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            comment, created = Comments.objects.get_or_create(
                review_id=row['review_id'],
                text=row['text'],
                author=row['author'],
                pub_date=row['pub_date'],
            )
            if created:
                print(f"Создан комментарий: {comment.text}")
            else:
                print(f"Комментарий уже существует: {comment.text}")

def import_genre_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            genre, created = Genre.objects.get_or_create(
                name=row['name'],
                slug=row['slug'],
            )
            if created:
                print(f"Создан жанр: {genre.name}")
            else:
                print(f"Жанр уже существует: {genre.name}")

def import_titlegenre_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            titlegenre, created = TitleGenre.objects.get_or_create(
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            if created:
                print(f"Создан: {titlegenre}")
            else:
                print(f"Уже существует: {titlegenre}")

def import_review_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            review, created = Reviews.objects.get_or_create(
                title_id=row['title_id'],
                text=row['text'],
                author=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            if created:
                print(f"Создан отзыв: {review}")
            else:
                print(f"Отзыв уже существует: {review}")

if __name__ == "__main__":
    # Укажите путь к вашему CSV файлу
    import_users_from_csv('api_yamdb/static/data/users.csv')
    import_titles_from_csv('api_yamdb/static/data/titles.csv')
    import_categories_from_csv('api_yamdb/static/data/category.csv')
    import_comments_from_csv('api_yamdb/static/data/comments.csv')
    import_genre_from_csv('api_yamdb/static/data/genre.csv')
    import_titlegenre_from_csv('api_yamdb/static/data/genre_title.csv')
    import_review_from_csv('api_yamdb/static/data/review.csv')
