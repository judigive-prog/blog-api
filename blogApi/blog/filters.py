import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    title = django_filters.CharFilter(field_name="title", lookup_expr='icontains')
    
    class Meta:
        model = Post
        fields = ['category__name', 'tags__name', 'author__username']