import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG, MIN_VALUE_VALIDAROR, MAX_VALUE_VALIDAROR, MAX_YEAR


class BaseModel(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH_NAME)
    slug = models.SlugField('Идентификатор', max_length=MAX_LENGTH_SLUG, unique=True)

    class Meta:
        abstract = True


class BaseContent(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(BaseModel):

    class Meta(BaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(BaseModel):

    class Meta(BaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey(
        'Title', on_delete=models.CASCADE, null=True,
    )
    genre_id = models.ForeignKey(
        Genre, on_delete=models.CASCADE, null=True,
    )


class Review(BaseContent):
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE_VALIDAROR, f'Оценка не может < {MIN_VALUE_VALIDAROR}'),
            MaxValueValidator(MAX_VALUE_VALIDAROR, f'Оценка не может > {MAX_VALUE_VALIDAROR}'),
        ],
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE, null=True,
        related_name='title_review'
    )

    class Meta:
        """Класс meta."""
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review')]


class Comment(BaseContent):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL, null=True,
        related_name='review_comments'
    )

    class Meta:
        """Класс meta."""
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    description = models.TextField('Описание')
    year = models.SmallIntegerField('Год', validators=[
            MaxValueValidator(MAX_YEAR, f'Год выпуска не может быть позднее {MAX_YEAR}'),
        ],)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre, through=TitleGenre, verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
