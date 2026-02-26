from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    message = 'siz sotuvchi emassiz'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_seller
    
class IsCustomer(BasePermission):
    message = 'siz xaridor emassiz'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer