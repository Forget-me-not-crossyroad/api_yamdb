from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.models import Users


def is_admin_user(request):
    if request.user.is_superuser:
        return 'admin'
    else:
        user = Users.objects.get(id=request.user.id, is_active=True)
        return user.role


class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_authenticated and
                is_admin_user(request) == 'admin'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if (request.user.is_authenticated and
                is_admin_user(request) == 'admin'):
            return True
        else:
            return False


class CommonTopicsPermissions(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                (request.user.is_authenticated and
                 is_admin_user(request) == 'admin'))

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
               (request.user.is_authenticated and
                is_admin_user(request) == 'admin'))


class ContentPermissions(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                is_admin_user(request) == 'admin' or
                is_admin_user(request) == 'moderator' or
                obj.author == request.user)
