from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        fields = ('name', 'year', 'genre', 'category')
        model = Title
