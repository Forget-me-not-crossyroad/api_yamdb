"""
Аноним — может просматривать описания произведений, читать отзывы и комментарии.

Аутентифицированный пользователь (user) — может читать всё, как и Аноним,
может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам),
может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии,
редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

Модератор (moderator) — те же права, что и у Аутентифицированного пользователя,
плюс право удалять и редактировать любые отзывы и комментарии.

Администратор (admin) — полные права на управление всем контентом проекта.
Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin.
Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора.
Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class CommonTopicsPermissions(BasePermission):

    def user_role(self, request):
        if request.user.is_superuser:
            return 'admin'
        else:
            return UserProfile.objects.get(user_id=request.user.id).fields('role')

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
            return UserProfile.objects.get(user_id=request.user.id).fields('role')

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
