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


class CategorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Category


class TitleSafeMethodsSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = fields


class TitleUnsafeMethodsSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review_id',)


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username',
    )

    def validate(self, data):
        request = self.context.get('request')
        if not (request.method == 'POST'):
            return data
        if Review.objects.filter(
                    title=get_object_or_404(
                        Title,
                        pk=self.context['view'].kwargs['title_id']
                    ), author=request.user).exists():
            raise serializers.ValidationError(
                    'Нельзя оставлять больше одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title_id',)
