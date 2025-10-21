from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow staff to edit, others read-only.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to access their own shipments, admins see all.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users can access any shipment
        if request.user.is_staff:
            return True
        
        # Users can access their own shipments via created_by
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        # For now, allow access if user is authenticated (can be refined later)
        return request.user.is_authenticated


class IsPublicTracking(permissions.BasePermission):
    """
    Allow public access to tracking endpoint.
    """
    
    def has_permission(self, request, view):
        return True  # Public access
