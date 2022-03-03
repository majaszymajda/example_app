import django_filters
from django_filters import FilterSet

from users.models import User


class UserFilters(FilterSet):

    last_name = django_filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    first_name = django_filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    username = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")


    class Meta:
        model = User

        fields = [
            "last_name",
            "first_name",
            "username",
            "email",
        ]

