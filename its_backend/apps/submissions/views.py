from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response

from ..permission_classes import IsStudent, IsTutor
from ..questions.models import Question
from .models import Submissiondata
from .serializers import (
    CreateUpdateSubmissionSerializer,
    RetrieveAllSubmissionSerializer,
    StudentRetrieveSubmissionDetailsSerializer,
    TutorRetrieveSubmissionDetailsSerializer,
)
from .utils import process_submission_request


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
        "create": CreateUpdateSubmissionSerializer,
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
        qn_id = request.data.get("qn_id")
        if qn_id is None:
            return Response(
                data={"message": "You need to supply a question id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 10))
        queryset = self.get_queryset().filter(qn_id=qn_id)
        submissions = queryset.order_by("submission_number")[offset : limit + offset]
        serializer = self.get_serializer_class()(submissions, many=True)
        return Response(
            data={"submissions": serializer.data}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        submission = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer_class()(submission)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TutorSubmissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Submissiondata.objects.all()
    permission_classes = (IsTutor,)
    serializer_class = {
        "list": RetrieveAllSubmissionSerializer,
        "retrieve": TutorRetrieveSubmissionDetailsSerializer,
        "partial_update": CreateUpdateSubmissionSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class.get(self.action)

    def get_queryset(self):
        # Filter for submissions to questions created by the authenticated user
        qn_id = self.request.query_params.get("qn_id")
        try:
            Question.objects.get(pk=qn_id, pub_by=self.request.user)
            return Submissiondata.objects.filter(qn_id=qn_id)
        except Question.DoesNotExist as err:
            raise PermissionDenied() from err

    def list(self, request):
        qn_id = request.query_params.get("qn_id")
        print(qn_id)
        if qn_id is None:
            return Response(
                data={"message": "You need to supply a question id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            queryset = self.get_queryset().order_by(
                "-submission_date", "submitted_by__email"
            )
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
            Question.objects.get(pk=submission.qn_id, pub_by=self.request.user)
            serializer = self.get_serializer_class()(submission)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Question.DoesNotExist:
            # If the question is not created by the authenticated user
            return Response(
                data={
                    "message": f"You do not have the permission to access information for submission {pk}"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        except Submissiondata.DoesNotExist:
            return Response(
                data={"message": "The submission requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def update(self, request, partial=True, pk=None):
        queryset = self.queryset
        submision_pk = pk
        try:
            submission = queryset.get(pk=submision_pk)
            Question.objects.get(pk=submission.qn_id, pub_by=self.request.user)
        except Question.DoesNotExist:
            # If the question is not created by the authenticated user
            return Response(
                data={
                    "message": f"You do not have the permission to access information for submission {pk}"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except Submissiondata.DoesNotExist:
            return Response(
                data={"message": "The submission requested does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

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
