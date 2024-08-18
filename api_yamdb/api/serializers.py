import datetime
import re
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comments, Reviews


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

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
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ('title_id', )
