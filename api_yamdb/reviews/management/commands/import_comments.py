import csv

from django.core.management.base import BaseCommand

from reviews.models import Comment


class Command(BaseCommand):
    help = 'Загружает файлы comments.csv в базу данных'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/comments.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                comment, created = Comment.objects.get_or_create(
                    review_id=row['review_id'],
                    text=row['text'],
                    author=row['author'],
                    pub_date=row['pub_date'],
                )
                if created:
                    self.stdout.write(f'Создан комментарий: {comment.text}')
                else:
                    self.stdout.write(
                        f'Комментарий уже существует: {comment.text}')
