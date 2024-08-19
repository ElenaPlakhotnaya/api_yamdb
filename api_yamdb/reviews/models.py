from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import User

class BaseModel(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        abstract = True


class BaseContent(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='author')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(BaseModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey('Title',
                                 on_delete=models.CASCADE, null=True,)
    genre_id = models.ForeignKey(Genre,
                                 on_delete=models.CASCADE, null=True,)


class Review(BaseContent):
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Оценка не может < 1'),
            MaxValueValidator(10, 'Оценка не может > 10'),
        ],
    )
    title = models.ForeignKey('Title',
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
                fields=["author", "title"], name="unique_review")]


class Comment(BaseContent):
    review_id = models.ForeignKey(Review,
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
    year = models.IntegerField('Год')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(Genre, through=TitleGenre,
                                   verbose_name='Жанр',)
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
