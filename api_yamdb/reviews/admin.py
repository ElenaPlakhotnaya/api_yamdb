from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class BaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review_id')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'title', 'score')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Category, BaseAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, BaseAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
