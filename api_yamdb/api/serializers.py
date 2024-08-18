import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comments, Reviews
from rest_framework.validators import UniqueValidator


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    # rating = serializers.IntegerField()
    
    class Meta:
        model = Title
        read_only_fields = ('raiting', )
        # fields = ('id', 'name', 'description', 'year', 'category', 'genre', 'rating')
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')

    def validate_year(self, value):
        year_today = datetime.datetime.now().year
        if value > year_today:
            raise serializers.ValidationError(
                f"Год выпуска не может быть позднее {year_today}."
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
    
    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Длина поля name не должна превышать 256 символов.'
            )
        return value
    
    def validate_slug(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(
                'Длина поля slug не должна превышать 50 символов.'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
    
    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Длина поля name не должна превышать 256 символов.'
            )
        return value
    
    def validate_slug(self, value):
        if len(value) > 50:
            raise serializers.ValidationError(
                'Длина поля slug не должна превышать 50 символов.'
            )
        return value

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review_id', )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', validators=[UniqueValidator(queryset=Reviews.objects.all(),
        message=("Name already exists"))]
    )

    
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews
        read_only_fields = ('id', )
        
       
