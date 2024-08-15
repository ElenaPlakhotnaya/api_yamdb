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
