from allauth.socialaccount.views import SignupView as AllauthSignupView
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponsePermanentRedirect
from rest_framework import generics, serializers, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..permission_classes import IsManager, IsStudent, IsTutor
from .models import CustomUser, Teaches
from .serializers import (
    RetrieveUserSerializer,
    SignInSerializer,
    SignUpSerializer,
    UpdateUserInfoSerializer,
)

# from .serializers import (SocialCallbackSerializer)


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class SignUpView(generics.CreateAPIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            serializer.save()
        except IntegrityError as e:
            return Response(
                data={"message": e.args}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(email=serializer.data["email"])
            tokens = generate_tokens_for_user(user)
            return Response(
                data={"tokens": tokens, "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        refresh_token = request.data["tokens"]["refresh_token"]
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refersh_token = RefreshToken(refresh_token)
            refersh_token.blacklist()
            logout(request)
            return Response(
                {"message": "User successfully logged out"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ["http", "https"]


""" 
Override allauth social signup view such that when a user attempts to third party signup with an existing email,
they gets logged in directly and redirected back to frontend
"""


class CustomSignupView(AllauthSignupView):
    http_method_names = ["get"]

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        social_login_email = self.sociallogin.user.email
        if CustomUser.objects.filter(email=social_login_email).exists():
            user = CustomUser.objects.get(email=social_login_email)
            tokens = generate_tokens_for_user(user)
            redirect_url = f'http://localhost:3000/en/auth/post-social-auth?access={tokens["access"]}&refresh={tokens["refresh"]}'
            return CustomRedirect(redirect_url)
        # TODO: What to do here?
        raise Exception()


class SocialCallbackView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user = request.user
        tokens = generate_tokens_for_user(user)
        redirect_url = f'http://localhost:3000/en/auth/post-social-auth?access={tokens["access"]}&refresh={tokens["refresh"]}'
        return CustomRedirect(redirect_url)


class RetrieveUserView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RetrieveUserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(instance=user)
        try:
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        """
        Example request:
        {
            "old_password": "sampleOldPassword123",
            "new_password": "sampleNewPassword456"
        }
        """

        # Get current user and payload data
        user: CustomUser = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # Check if old_password and new_password are provided in request data
        if not old_password or not new_password:
            return Response(
                {"error": "Old password and new password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify old password
        if not user.check_password(old_password):
            return Response(
                {"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )


class RetrieveStudentsView(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RetrieveUserSerializer

    def get_student_by_id(self, student_id: str):
        """
        Example response (one serialized CustomUser in JSON)
        {
            "user": serialized_CustomUser1
        }
        """
        if not student_id.isdigit():
            return Response(
                {"error": "Student ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student_id: int = int(student_id)

        # TODO: Bulk GET students does not throw error if student is not found or user is not a student
        #       (should this do the same?)
        try:
            student = CustomUser.objects.get(id=student_id)
            if not student.is_student:
                return Response(
                    data={"error": f"User with id {student_id} is not a student"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ObjectDoesNotExist:
            return Response(
                data={"error": f"Student with id {student_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            serialized_data = self.serializer_class(student).data
        except serializers.ValidationError as e:
            return Response(
                data={"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": serialized_data}, status=status.HTTP_200_OK)

    def get_students_by_ids(self, student_ids: list[str]):
        """
        Example response (list of serialized CustomUser in JSON)
        {
            "user": [
                serialized_CustomUser1,
                serialized_CustomUser2,
                ...
            ]
        }
        """
        if len(student_ids) == 1 and "," in student_ids[0]:
            student_ids = student_ids[0].replace(" ", "").split(",")

        try:
            student_ids: list[int] = [int(s_id) for s_id in student_ids]
        except ValueError:
            return Response(
                {"error": "Student ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        students = CustomUser.objects.filter(id__in=student_ids)
        try:
            serialized_data = [
                self.serializer_class(s).data for s in students if s.is_student
            ]
        except serializers.ValidationError as e:
            return Response(
                data={"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": serialized_data}, status=status.HTTP_200_OK)

    def get_students_by_tutor(self, tutor_id: str, invert: str):
        """
        Example response (list of serialized CustomUser in JSON)
        {
            "user": [
                serialized_CustomUser1,
                serialized_CustomUser2,
                ...
            ]
        }
        """
        if not tutor_id.isdigit():
            return Response(
                {"error": "Tutor ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tutor_id: int = int(tutor_id)
        invert: bool = invert.lower() == "true"

        students_taught_by_tutor = Teaches.objects.filter(tutor=tutor_id).values_list(
            "student", flat=True
        )
        if invert:
            students = CustomUser.objects.exclude(
                id__in=students_taught_by_tutor
            ).filter(is_student=True)
        else:
            students = CustomUser.objects.filter(id__in=students_taught_by_tutor)

        try:
            serialized_data = [self.serializer_class(s).data for s in students]
        except serializers.ValidationError as e:
            return Response(
                data={"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": serialized_data}, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest):
        """
        Example url query string
        1. /students?student_id=1
        2. /students?student_ids=1,2,3
        3. /students?student_ids=1&student_ids=2&student_ids=3
        4. /students?tutor_id=10
        5. /students?tutor_id=10&invert=true

        Example response for each query (assuming all are valid queries)
        1. CustomUser with id=1 and is_student=True
        2. Three CustomUsers with id in (1, 2, 3) and is_student=True
        3. Same as the above
        4. n CustomUsers that are taught by tutor with id=10
        5. m CustomUsers that are NOT taught by tutor with id=10
            -> so that tutors can potentially add them in their class (?)

        If multiple GET params are specified, it will be evaluated in the
        order mentioned above
        """
        url_query = request.GET
        student_id = url_query.get("student_id")
        student_ids = url_query.getlist("student_ids")
        tutor_id = url_query.get("tutor_id")
        invert = url_query.get("invert", default="false")

        if student_id:
            return self.get_student_by_id(student_id)
        if student_ids:
            return self.get_students_by_ids(student_ids)
        if tutor_id:
            return self.get_students_by_tutor(tutor_id, invert)

        return Response(
            {"error": "No student or tutor ids provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RetrieveTutorsView(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RetrieveUserSerializer

    def get_tutor_by_id(self, tutor_id: str):
        """
        Example response (one serialized CustomUser in JSON)
        {
            "user": serialized_CustomUser1
        }
        """
        if not tutor_id.isdigit():
            return Response(
                {"error": "Tutor ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tutor_id: int = int(tutor_id)

        # TODO: Bulk GET tutors does not throw error if tutor is not found or user is not a tutor
        #       (should this do the same?)
        try:
            tutor = CustomUser.objects.get(id=tutor_id)
            if not tutor.is_tutor:
                return Response(
                    data={"error": f"User with id {tutor_id} is not a tutor"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ObjectDoesNotExist:
            return Response(
                data={"error": f"Tutor with id {tutor_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            serialized_data = self.serializer_class(tutor).data
        except serializers.ValidationError as e:
            return Response(
                data={"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": serialized_data}, status=status.HTTP_200_OK)

    def get_tutors_by_ids(self, tutor_ids: list[str]):
        """
        Example response (list of serialized CustomUser in JSON)
        {
            "user": [
                serialized_CustomUser1,
                serialized_CustomUser2,
                ...
            ]
        }
        """
        if len(tutor_ids) == 1 and "," in tutor_ids[0]:
            tutor_ids = tutor_ids[0].replace(" ", "").split(",")

        try:
            tutor_ids: list[int] = [int(t_id) for t_id in tutor_ids]
        except ValueError:
            return Response(
                {"error": "Tutor ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tutors = CustomUser.objects.filter(id__in=tutor_ids)
        try:
            serialized_data = [
                self.serializer_class(t).data for t in tutors if t.is_tutor
            ]
        except serializers.ValidationError as e:
            return Response(
                data={"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": serialized_data}, status=status.HTTP_200_OK)

    def get_tutors_of_student(self, student_id: str):
        """
        Example response (list of serialized CustomUser in JSON)
        {
            "user": [
                serialized_CustomUser1,
                serialized_CustomUser2,
                ...
            ]
        }
        """
        if not student_id.isdigit():
            return Response(
                {"error": "Student ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student_id: int = int(student_id)
        tutors_of_student = Teaches.objects.filter(student=student_id).select_related(
            "tutor"
        )

        try:
            serialized_data = [
                self.serializer_class(t.tutor).data for t in tutors_of_student
            ]
        except serializers.ValidationError as e:
            return Response(
                data={"error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"user": serialized_data}, status=status.HTTP_200_OK)

    def get(self, request: HttpRequest):
        """
        Example url query string
        1. /tutors?tutor_id=10
        2. /tutors?tutor_ids=10,20,30
        3. /tutors?tutor_ids=10&tutor_ids=20&tutor_ids=30
        4. /tutors?student_id=1

        Example response for each query (assuming all are valid queries)
        1. CustomUser with id=10 and is_tutor=True
        2. Three CustomUsers with id in (10, 20, 30) and is_tutor=True
        3. Same as the above
        4. n CustomUsers that teach student with id=1

        If multiple GET params are specified, it will be evaluated in the
        order mentioned above
        """
        url_query = request.GET
        tutor_id = url_query.get("tutor_id")
        tutor_ids = url_query.getlist("tutor_ids")
        student_id = url_query.get("student_id")

        if tutor_id:
            return self.get_tutor_by_id(tutor_id)
        if tutor_ids:
            return self.get_tutors_by_ids(tutor_ids)
        if student_id:
            return self.get_tutors_of_student(student_id)

        return Response(
            {"error": "No student or tutor ids provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AddTutorStudentRelationshipView(views.APIView):
    permission_classes = [IsManager | IsTutor]

    def post(self, request: HttpRequest):
        """
        Example payload
        {
            "tutor_id": 10,
            "student_ids": [1, 2, 3]
        }
        """
        payload = request.data
        tutor_id = payload.get("tutor_id")
        student_ids = payload.get("student_ids")

        if not tutor_id or not student_ids:
            return Response(
                {"error": "Tutor ID and student ID(s) must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            not isinstance(tutor_id, int)
            or not isinstance(student_ids, list)
            or any(not isinstance(s_id, int) for s_id in student_ids)
        ):
            return Response(
                {"error": "Tutor ID and student ID(s) must be integers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        messages = []  # students successfully added
        errors = []  # students not successfully added
        for s_id in student_ids:
            ok, error_msg = Teaches.objects.add_teaching_relationship(tutor_id, s_id)
            if ok:
                # e.g., "Added [tutor_id=10, s_id=1]"
                messages.append(f"Added [{tutor_id=}, {s_id=}]")
            else:
                # e.g., "[tutor_id=10, s_id=1]: UNIQUE constraint failed: R.tutor_id, R.student_id"
                errors.append(f"[{tutor_id=}, {s_id=}]: {error_msg}")

        response = {}
        if messages:
            response |= {"message": messages}
        if errors:
            response |= {"error": errors}

        return Response(response, status=status.HTTP_200_OK)


class UpdateUserInfoView(generics.UpdateAPIView):
    permission_classes = [IsStudent | IsTutor]
    serializer = UpdateUserInfoSerializer

    def patch(self, request, partial=True):
        serializer = self.serializer(request.user, request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
