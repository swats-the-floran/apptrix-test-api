from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):

    def has_permission(self, request, view):
        print(view.action)
        if view.action == 'create':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action == 'match':
            return request.user.is_authenticated

        return False
