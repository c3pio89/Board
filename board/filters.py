
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter
from django.forms import DateTimeInput


class CommentFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Text',
    )