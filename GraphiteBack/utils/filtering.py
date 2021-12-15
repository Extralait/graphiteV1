from django.db.models import QuerySet
from rest_framework_filters.backends import ComplexFilterBackend


class CustomizedBackend(ComplexFilterBackend):
    operators = {
        '&': QuerySet.intersection,
        '|': QuerySet.union,
        '-': QuerySet.difference,
    }
