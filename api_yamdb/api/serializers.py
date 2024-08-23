from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Genre
        fields = (
            'name',
            'slug'
        )


class CategorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Category
        fields = (
            'name',
            'slug'
        )


class TitleSafeMethodsSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(
            Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return None

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class TitleUnsafeMethodsSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True,
                                         required=True,
                                         allow_empty=False)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )

    def to_representation(self, instance):
        return TitleSafeMethodsSerializer(instance).data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title_id',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        if Review.objects.filter(
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs['title_id']
                ), author=request.user).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять больше одного отзыва на произведение')
        return data
