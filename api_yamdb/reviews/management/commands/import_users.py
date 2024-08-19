from django.core.management.base import BaseCommand
from users.models import User  
import csv

class Command(BaseCommand):
    help = 'Загружает файлы users.csv в базу данных'
    def handle(self, *args, **kwargs):
        file_path = 'static/data/users.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user, created = User.objects.get_or_create(
                    id=row['id'],
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
               
            