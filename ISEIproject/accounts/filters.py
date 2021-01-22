import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


# filter activities on the teacher page
class PDAInstanceFilterTeacher(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte')
    summary = CharFilter(field_name='summary', lookup_expr='icontains')

    class Meta:
        model = PDAInstance
        fields = '__all__'
        exclude = ['teacher', 'date']


# filter activities on the PDAInstance page
class PDAInstanceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte')
    summary = CharFilter(field_name='summary', lookup_expr='icontains')

    class Meta:
        model = PDAInstance
        fields = '__all__'
        exclude = ['date']


# filter teachers
class TeacherFilter(django_filters.FilterSet):
    # school = CharFilter(field_name = 'school', lookup_expr = 'icontains')

    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user', 'phone', 'profile_picture']
