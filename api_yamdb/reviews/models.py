from django.db import models
from django.contrib.auth import get_user_model

from users.models import User

class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey('Title',
                                 on_delete=models.SET_NULL, null=True,)
    genre_id = models.ForeignKey(Genre,
                                 on_delete=models.SET_NULL, null=True,)


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    description = models.TextField('Описание')
    year = models.IntegerField('Год')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre, through=TitleGenre,
                                   verbose_name='Жанр',)  # сомневаюсь в этом поле
    # rewiew = models.ForeignKey(
    #    Review,
    #    on_delete=models.SET_NULL, null=True,
    # )  в документации не увидела. нужен ли?
    raiting = models.FloatField('Рейтинг', null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey('Title',
                                 on_delete=models.SET_NULL, null=True,)
    genre_id = models.ForeignKey(Genre,
                                 on_delete=models.SET_NULL, null=True,)


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    description = models.TextField('Описание')
    year = models.IntegerField('Год')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre, through=TitleGenre,
                                   verbose_name='Жанр',)  # сомневаюсь в этом поле
    # rewiew = models.ForeignKey(
    #    Review,
    #    on_delete=models.SET_NULL, null=True,
    # )  в документации не увидела. нужен ли?
    raiting = models.FloatField('Рейтинг', null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
