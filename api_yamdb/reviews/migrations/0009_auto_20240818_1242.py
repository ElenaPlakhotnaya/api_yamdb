# Generated by Django 3.2 on 2024-08-18 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_remove_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titlegenre',
            name='genre_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.genre'),
        ),
        migrations.AlterField(
            model_name='titlegenre',
            name='title_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.title'),
        ),
    ]
