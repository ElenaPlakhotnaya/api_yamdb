import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comments, Reviews


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
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


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
