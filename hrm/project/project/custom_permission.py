from rest_framework.permissions import BasePermission


class IsHREmployee(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user) and (request.user.is_hr==True)