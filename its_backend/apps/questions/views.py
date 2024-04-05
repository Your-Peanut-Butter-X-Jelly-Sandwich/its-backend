from datetime import date, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.response import Response

from ...apps.accounts.models import Teaches
from ..accounts.models import CustomUser
from ..accounts.serializers import RetrieveUserSerializer
from ..permission_classes import IsStudent, IsTutor
from ..questions.models import Question
from ..submissions.models import Submissiondata
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

    def get_total_assignees(self, tutor):
        return Teaches.objects.filter(tutor=tutor).count()

    def get_total_submissions(self, qn_id, tutor):
        students = Teaches.objects.filter(tutor=tutor).values("student")
        return Submissiondata.objects.filter(
            qn_id=qn_id, submitted_by__in=students
        ).count()

    def get_total_passes(self, qn_id, tutor):
        students = Teaches.objects.filter(tutor=tutor).values("student")
        all_submissions = Submissiondata.objects.filter(
            qn_id=qn_id, submitted_by__in=students
        )
        # total_test_cases = TestCase.objects.filter(question__pk=qn_id).count()

        passing_submissions = all_submissions.filter(score=F("total_score"))
        distinct_passing_submissions = (
            passing_submissions.values("submitted_by").distinct().count()
        )
        return distinct_passing_submissions

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        question = get_object_or_404(queryset, pk=pk)
        total_submissions = self.get_total_submissions(
            pk, request.user
        )  # each student can make multiple submissions, so this number can be greater than student count
        passes = self.get_total_passes(
            pk, request.user
        )  # each student can only pass once, so this number must be smaller than student count
        total_students = self.get_total_assignees(request.user)
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
        questions = queryset.order_by("-pub_date")[offset : offset + limit]
        serializer = self.get_serializer_class()(
            questions, many=True, context={"user": request.user}
        )
        return Response(data={"questions": serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset()
        question = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer_class()(question)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StudentDashboardStatisticsView(generics.RetrieveAPIView):
    permission_classes = [
        IsStudent,
    ]

    def get_personal_info(self, student):
        serializer = RetrieveUserSerializer(student)
        return serializer.data

    def get_tutors(self, student):
        tutors = Teaches.objects.filter(student=student).values("tutor")
        return tutors

    def get_tutor_list(self, tutors):
        tutor_ids = tutors.values("tutor_id")
        tutors = CustomUser.objects.filter(pk__in=tutor_ids)
        serializer = RetrieveUserSerializer(tutors, many=True)
        return serializer.data

    def get_all_questions_assigned(self, tutors):
        questions = Question.objects.filter(pub_by__in=tutors)
        count = questions.count()
        return questions, count

    def get_attempted_questions_count(self, student):
        submissions = (
            Submissiondata.objects.filter(submitted_by=student)
            .values("qn_id")
            .distinct()
        )
        count = submissions.count()
        return count

    def get_due_questions(self, questions, student):
        questions_due_in_a_week = questions.filter(
            due_date__lte=date.today() + timedelta(weeks=1), due_date__gte=date.today()
        ).order_by("due_date")
        serializer_week = StudentQuestionListSerializer(
            questions_due_in_a_week, many=True, context={"user": student}
        )
        questions_due_in_a_month = questions.filter(
            due_date__lte=date.today() + timedelta(days=30), due_date__gte=date.today()
        ).order_by("due_date")
        serializer_month = StudentQuestionListSerializer(
            questions_due_in_a_month, many=True, context={"user": student}
        )

        return serializer_week.data, serializer_month.data

    def get(self, request):
        student = request.user
        personal_info = self.get_personal_info(student)
        tutors = self.get_tutors(student)
        tutor_list = self.get_tutor_list(tutors)
        questions, total_questions_count = self.get_all_questions_assigned(tutors)
        attempted_questions_count = self.get_attempted_questions_count(student)
        due_in_week, due_in_month = self.get_due_questions(questions, student)
        data = {
            "personal_info": personal_info,
            "tutors": tutor_list,
            "total_question_assigned": total_questions_count,
            "attempted_questions": attempted_questions_count,
            "questions_due_in_a_week": due_in_week,
            "questions_due_in_a_month": due_in_month,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TutorDashboardStatisticsView(generics.RetrieveAPIView):
    permission_classes = [
        IsTutor,
    ]

    def get_personal_info(self, tutor):
        serializer = RetrieveUserSerializer(tutor)
        return serializer.data

    def get_students(self, tutor):
        students = Teaches.objects.filter(tutor=tutor).values("student")
        return students

    def get_student_list(self, students):
        for s in students.values():
            print(s)
        students_ids = students.values("student_id")
        students = CustomUser.objects.filter(pk__in=students_ids)
        serializer = RetrieveUserSerializer(students, many=True)
        return serializer.data

    def get_all_questions_created(self, tutor):
        questions = Question.objects.filter(pub_by=tutor)
        return questions

    def get_questions_due(self, questions):
        questions_due_in_a_week = questions.filter(
            due_date__lte=date.today() + timedelta(weeks=1), due_date__gte=date.today()
        ).order_by("due_date")
        serializer_week = TutorQuestionListSerializer(
            questions_due_in_a_week, many=True
        )
        questions_due_in_a_month = questions.filter(
            due_date__lte=date.today() + timedelta(days=30), due_date__gte=date.today()
        ).order_by("due_date")
        serializer_month = TutorQuestionListSerializer(
            questions_due_in_a_month, many=True
        )

        return serializer_week.data, serializer_month.data

    def get(self, request):
        tutor = request.user
        personal_info = self.get_personal_info(tutor)
        students = self.get_students(tutor)
        student_list = self.get_student_list(students)
        questions = self.get_all_questions_created(tutor)
        due_in_week, due_in_month = self.get_questions_due(questions)
        data = {
            "personal_info": personal_info,
            "students": student_list,
            "questions_due_in_a_week": due_in_week,
            "questions_due_in_a_month": due_in_month,
        }
        return Response(data=data, status=status.HTTP_200_OK)
