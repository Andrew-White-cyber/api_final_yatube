from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Допуск на уровне объекта.
    Изменение только для автора объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
