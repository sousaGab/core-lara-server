from rest_framework import permissions

class IsAdminOrOwnerUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        is_auth = (obj.user == request.user or request.user.is_staff)
        
        return is_auth