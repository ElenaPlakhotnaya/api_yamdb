from django.db import models
from django.db.models import Avg
from django.core.exceptions import ValidationError
from users.models import User
from django.http import HttpResponseBadRequest

class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def str(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def str(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey('Title',
                                 on_delete=models.SET_NULL, null=True )
    genre_id = models.ForeignKey(Genre,
                                 on_delete=models.SET_NULL, null=True)


class Reviews(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    score = models.IntegerField('Оценка')
    pub_date = models.DateTimeField('Дата отзывы', auto_now_add=True)
    title_id = models.ForeignKey('Title',
                                 on_delete=models.SET_NULL, null=True, related_name='title_review')

    class Meta:
        """Класс meta."""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    #def validate_unique(self, exclude=None):
        #qs = Reviews.objects.filter(title_id=self.title_id)
        #if qs.filter(author=self.author):
            #raise ValueError('hbjhjh')

    #def save(self, *args, **kwargs):
        #self.validate_unique()
        #super(Reviews. self).save(*args, **kwargs)


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commet_author')
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)
    review_id = models.ForeignKey(Reviews,
                                  on_delete=models.SET_NULL, null=True, related_name='review_comments')

    class Meta:
        """Класс meta."""

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    description = models.TextField('Описание')
    year = models.IntegerField('Год')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория', related_name='category'
    )
    genre = models.ManyToManyField(Genre, through=TitleGenre,
                                   verbose_name='Жанр', related_name='genre')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def str(self):
        return self.name
    