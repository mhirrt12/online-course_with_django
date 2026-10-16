import django_filters
from course.models import Course
class CourseFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date__gte'
    )

    created_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date__lte'
    )

    class Meta:
        model = Course
        fields = {
            'category__name': ['exact', 'icontains'],
        }
