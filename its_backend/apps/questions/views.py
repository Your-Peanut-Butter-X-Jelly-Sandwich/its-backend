from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response

from ...apps.accounts.models import Teaches
from ..permission_classes import IsStudent, IsTutor
from .models import Question
from .serializers import (
    StudentQuestionDetailSerializer,
    StudentQuestionListSerializer,
    TutorCreateUpdateQuestionSerializer,
    TutorQuestionDetailSerializer,
    TutorQuestionListSerializer,
)

# Comment unused imports for now
# from .models import TestCase
# from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


class TutorQuestionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Question.objects.all()
    permission_classes = (IsTutor,)
    serializer_classes = {
        "list": TutorQuestionListSerializer,
        "retrieve": TutorQuestionDetailSerializer,
        "create": TutorCreateUpdateQuestionSerializer,
        "update": TutorCreateUpdateQuestionSerializer,
        "partial_update": TutorCreateUpdateQuestionSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        return self.queryset.filter(pub_by=self.request.user)

    def create(self, request):
        serializer = self.get_serializer_class()(
            data=request.data,
            context={"user": request.user},
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, partial=False, pk=None):
        queryset = self.get_queryset()
        question = queryset.get(pk=pk)
        serializer = self.get_serializer_class()(
            question,
            data=request.data,
            context={
                "pk": pk,
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

    def list(self, request):
        queryset = self.get_queryset()
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 10))
        questions = queryset.order_by("-pub_date")[offset : offset + limit]
        serializer = self.get_serializer_class()(questions, many=True)
        return Response(data={"questions": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        question = get_object_or_404(queryset, pk=pk)
        total_submissions = 100  # each student can make multiple submissions, so this number can be greater than student count
        passes = 20  # each student can only pass once, so this number must be smaller than student count
        total_students = Teaches.objects.filter(tutor=request.user).count()
        serializer = self.get_serializer_class()(question)
        return Response(
            data={
                "question": serializer.data,
                "total_students": total_students,
                "passes": passes,
                "total_submissions": total_submissions,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        try:
            question = queryset.get(pk=pk)
            question.delete()
            return Response(
                data={"message": f"question {pk} deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ObjectDoesNotExist:
            return Response(
                data={"message": f"question {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class StudentQuestionViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Question.objects.all()
    permission_classes = (IsStudent,)
    serializer_classes = {
        "list": StudentQuestionListSerializer,
        "retrieve": StudentQuestionDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        teaches_rel = Teaches.objects.filter(student=self.request.user)
        tutors = teaches_rel.values_list("tutor", flat=True)
        print(tutors)
        return self.queryset.filter(pub_by__in=tutors)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 10))
        # student = request.user
        # tutors = Teaches.objects.filter(student=student)
        questions = queryset.order_by("-pub_date")[offset : offset + limit]
        serializer = self.get_serializer_class()(questions, many=True)
        return Response(data={"questions": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset()
        question = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer_class()(question)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
