from rest_framework import serializers

from reviews.models import Title, Category, Genre

class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'category', 'genre',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'