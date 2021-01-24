import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter, BooleanFilter

from .models import *


class PDAInstanceFilter(django_filters.FilterSet):
    teacher = CharFilter(field_name = "pda_record__teacher", label='teacher')
    start_date = DateFilter(field_name="date_completed", lookup_expr='gte', label='Completed after:')
    end_date = DateFilter(field_name="date_completed", lookup_expr='lte', label='Completed before:')
    description = CharFilter(field_name='description', lookup_expr='icontains', label='Description')
    school_year = CharFilter(field_name='pda_record__school_year', label='School Year')
    CHOICES = (
        (None, 'Pending'),
        (True, 'Approved'),
        (False, 'Not Approved'),
    )
    principal_signature = ChoiceFilter(field_name='pda_record__principal_signature', label='Principal signed', )
    approved = ChoiceFilter(field_name='approved',label='Approved', choices = CHOICES)



class TeacherFilter(django_filters.FilterSet):
    # school = CharFilter(field_name = 'school', lookup_expr = 'icontains')

    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user', 'phone', 'profile_picture']
