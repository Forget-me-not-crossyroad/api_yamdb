from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.models import Users


def get_user_role(request):
    if request.user.is_superuser:
        return 'admin'
    else:
        user = Users.objects.get(id=request.user.id, is_active=True)
        return user.role


class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and get_user_role(request) == 'admin')


class CommonTopicsPermissions(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and get_user_role(request) == 'admin')


class ContentPermissions(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or get_user_role(request) == 'admin'
                or get_user_role(request) == 'moderator'
                or obj.author == request.user)
