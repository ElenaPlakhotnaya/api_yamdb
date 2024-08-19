import datetime
import re
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comments, Reviews
from rest_framework.validators import UniqueValidator
from django.db.models import Avg


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
        pattern = r'^[-a-zA-Z0-9_]+$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
            'Убедитесь, что используются только допустимые символы'
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
        pattern = r'^[-a-zA-Z0-9_]+$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Убедитесь, что используются только допустимые символы'
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
        read_only='True', slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews
        read_only_fields = ('id', )

    def validate(self, data):
        title_id = self.context.get(
            'request'
        ).parser_context['kwargs']['id']
        author = self.context.get('request').user
        this_title = Reviews.objects.all()
        if this_title.filter(author=author, title_id=title_id):
            raise serializers.ValidationError(
                'Нельзя оставлять два отзыва к одному фильму.'
            )
        return data
        
class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        read_only=True, many=True
    )
    rating = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'rating', 'category', 'genre')

    def get_rating(self, obj):
        reviews = obj.title_review.all()
        if reviews:
            result = reviews.aggregate(Avg('score'))['score__avg']
            return int(result)
        return None



class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='name', many=True, queryset=Genre.objects.all(), allow_empty=False
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')

    def validate_year(self, value):
        year_today = datetime.datetime.now().year
        if value > year_today:
            raise serializers.ValidationError(
                f"Год выпуска не может быть позднее {year_today}."
            )
        return value
    
    def to_representation(self, instance):
        return TitleListSerializer(instance).data
