from django.db import models


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
=======
from django.db import models



class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

class GenresTitles(models.Model):
    title_id = models.ForeignKey(Genres,
                                 on_delete=models.SET_NULL, null=True,)
    genre_id =  models.ForeignKey('Titles',
                                  on_delete=models.SET_NULL, null=True,)    

class Reviews(models.Model):
    pass

class Comments(models.Model):
    pass

class Titles(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL, null=True,
    )
    rewiew = models.OneToOneField(
        Reviews,  
        on_delete=models.SET_NULL, null=True,
    ) #в документации не увидела. нужен ли?
    #raiting = не поняла