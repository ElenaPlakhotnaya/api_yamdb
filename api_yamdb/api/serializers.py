from rest_framework import serializers

from reviews.models import Titles, Categories, Genres

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'