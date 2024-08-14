from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

class GenresTitles(models.Model):
    title_id = models.ForeignKey(Genres,
                                 on_delete=models.SET_NULL, null=True,)
    genre_id = models.ForeignKey('Titles',
                                  on_delete=models.SET_NULL, null=True,)    

class Reviews(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата отзывы', auto_now_add=True)
    title_id = models.ForeignKey('Titles',
                                 on_delete=models.SET_NULL, null=True,)
 
    class Meta:
        """Класс meta."""

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commet_author')
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)
    review_id = models.ForeignKey(Reviews,
                                 on_delete=models.SET_NULL, null=True,)

    class Meta:
        """Класс meta."""

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class Titles(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL, null=True,
    )
    rewiew = models.ForeignKey(
        Reviews,
        on_delete=models.SET_NULL, null=True,
    )  #в документации не увидела. нужен ли?