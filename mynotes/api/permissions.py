from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.owners and request.user in obj.owners.all())
    
class IsMember(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.members and request.user in obj.members.all())