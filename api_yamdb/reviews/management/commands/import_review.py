import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Загружает файлы review.csv в базу данных'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/review.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                review, created = Review.objects.get_or_create(
                    title_id=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                if created:
                    print(f"Создан отзыв: {review}")
                else:
                    print(f"Отзыв уже существует: {review}")
