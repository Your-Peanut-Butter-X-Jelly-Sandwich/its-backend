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


# from rest_framework.response import Response

# def require_tutor_permission(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_tutor:
#             return view_func(request, *args, **kwargs)
#         else:
#             return Response(data={"message": "You are not authorized to access this resource"}, status=401)
#     return wrapper_func

# def require_student_permission(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_student:
#             return view_func(request, *args, **kwargs)
#         else:
#             return Response(data={"message": "You are not authorized to access this resource"}, status=401)
#     return wrapper_func

# def require_administrator_permission(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_manager:
#             return view_func(request, *args, **kwargs)
#         else:
#             return Response(data={"message": "You are not authorized to access this resource"}, status=401)
#     return wrapper_func
