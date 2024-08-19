from django.core.management.base import BaseCommand
from reviews.models import Category
import csv


class Command(BaseCommand):
    help = 'Загружает файлы category.csv в базу данных'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/category.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                category, created = Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                if created:
                    print(f"Создана категория: {category.name}")
                else:
                    print(f"Категория уже существует: {category.name}")
