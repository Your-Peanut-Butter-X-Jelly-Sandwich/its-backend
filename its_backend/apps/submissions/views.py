from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied, BadRequest
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response
from ..permission_classes import IsStudent, IsTutor
from .models import Submissiondata
from ..questions.models import Question
from .serializers import (
    CreateSubmissionSerializer,
    CreateUpdateSubmissionSerializer,
    RetrieveAllSubmissionSerializer,
    TutorRetrieveSubmissionDetailsSerializer,
    StudentRetrieveSubmissionDetailsSerializer,
)
from .utils import process_submission_request

# Uncomment unused imports for now
# from django.contrib.auth.decorators import login_required
# from rest_framework import generics, mixins, serializers, status, views, viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from ..permission_classes import IsStudent, IsTutor
# from .its_system import its_request_feedback_fix, its_request_parser
# from .its_utils import (
#     its_request_feedback_fix,
#     its_request_parser,
#     its_request_parser_fncs_value,
# )


class StudentSubmissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Submissiondata.objects.all()
    permission_classes = (IsStudent,)
    serializer_class = {
        "list": RetrieveAllSubmissionSerializer,
        "retrieve": StudentRetrieveSubmissionDetailsSerializer,
        "create": CreateSubmissionSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class.get(self.action)

    def get_queryset(self):
        return self.queryset.filter(submitted_by=self.request.user)

    def create(self, request):
        try:
            its_processed_request = process_submission_request(request)
            serializer = self.get_serializer_class()(
                data=its_processed_request,
                context={"user": request.user},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request):
        print("in list")
        qn_id = request.data.get("qn_id")
        # offset = request.query_params.get("offset", 0)
        # limit = request.query_params.get("limit", 10)
        queryset = self.get_queryset().filter(qn_id=qn_id)
        submissions = queryset.order_by("submission_number")
        serializer = self.get_serializer_class()(submissions, many=True)
        return Response(
            data={"submissions": serializer.data}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        submission = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer_class()(submission, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TutorSubmissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    print("in tutor view")
    queryset = Submissiondata.objects.all()
    permission_classes = (IsTutor,)
    serializer_class = {
        "list": RetrieveAllSubmissionSerializer,
        "retrieve": TutorRetrieveSubmissionDetailsSerializer,
        "partial_update": CreateUpdateSubmissionSerializer,
    }
    print("got here", serializer_class)

    def get_serializer_class(self):
        print("self.action", self.action)
        return self.serializer_class.get(self.action)

    def get_queryset(self):
        # Filter for submissions to questions created by the authenticated user
        qn_id = self.request.query_params.get("qn_id")
        if qn_id == None:
            raise BadRequest("You need to supply a question id")
        # Check that the question requested is created by the authenticated user
        try:
            question = Question.objects.get(pk=qn_id, pub_by=self.request.user)
            return Submissiondata.objects.filter(qn_id=qn_id)
        except Question.DoesNotExist:
            raise PermissionDenied()

    # def create(self, request):

    def list(self, request):
        qn_id = self.request.query_params.get("qn_id")
        if qn_id == None:
            return Response(
                data={"message": "You need to supply a question id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            queryset = self.get_queryset().order_by(
                "-submission_date", "submitted_by__email"
            )
            print(queryset)
            serializer = self.get_serializer_class()(queryset, many=True)
            return Response(
                data={"submissions": serializer.data}, status=status.HTTP_200_OK
            )
        except PermissionDenied:
            return Response(
                data={
                    "message": f"You do not have the permission to access information for question {qn_id}"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk):
        queryset = self.queryset
        try:
            submission = queryset.get(pk=pk)
            question = Question.objects.get(
                pk=submission.qn_id, pub_by=self.request.user
            )
            serializer = self.get_serializer_class()(submission)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Submissiondata.DoesNotExist:
            return Response(
                data={"message": "the submission requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Question.DoesNotExist:
            return Response(
                data={
                    "message": f"You do not have the permission to access information for submission {pk}"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, partial=True, pk=None):
        print("in update")
        queryset = self.get_queryset()
        submision_pk = pk
        submission = queryset.get(pk=submision_pk)
        serializer = self.get_serializer_class()(
            submission,
            data=request.data,
            context={
                "pk": submision_pk,
                "user": request.user,
            },
            partial=partial,
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
