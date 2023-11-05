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
        if request.user.is_authenticated and is_admin_user(request) == 'admin':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and is_admin_user(request) == 'admin':
            return True
        else:
            return False
        # return obj.author == request.user or request.user.is_superuser


class CommonTopicsPermissions(BasePermission):

    def user_role(self, request):
        if request.user.is_superuser:
            return 'admin'
        else:
            return Users.objects.get(user_id=request.user.id).fields('role')

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                self.user_role(request) == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                self.user_role(request) == 'admin')


class ContentPermissions(BasePermission):

    def user_role(self, request):
        if request.user.is_superuser:
            return 'admin'
        else:
            return Users.objects.get(user_id=request.user.id).fields('role')

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                self.user_role(request) == 'admin' or
                obj.author == request.user)

class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated and request.user.is_superuser)


class AuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
