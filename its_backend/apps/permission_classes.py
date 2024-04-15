from rest_framework import permissions


class IsTutor(permissions.BasePermission):
    message = "Only tutors are authorized to access this resource"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_tutor


class IsStudent(permissions.BasePermission):
    message = "Only students are authorized to access this resource"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsManager(permissions.BasePermission):
    message = "Only administrators are authorized to access this resource"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager
