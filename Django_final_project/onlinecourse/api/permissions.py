from rest_framework.permissions import BasePermission


class IsInstructorOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        profile = getattr(request.user, 'profile', None)

        return profile and profile.role == 'instructor'