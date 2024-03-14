<<<<<<< HEAD
from rest_framework import generics, views, viewsets,  mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Submissiondata
from .serializers import RetrieveSubmissionDetailsSerializer, RetrieveAllSubmissionSerializer, CreateSubmissionSerializer
from django.contrib.auth.decorators import login_required
from .its_utils import its_request_parser_fncs_value, its_request_parser, its_request_feedback_fix
from ..permission_classes import IsStudent, IsTutor
from rest_framework import serializers
from .utils import process_submission_request
from django.shortcuts import get_object_or_404
=======
from rest_framework import views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Submissiondata
from .serializers import RetrieveSubmissionSerializer, CreateSubmissionSerializer
from .its_system import its_request_parser, its_request_feedback_fix

# Uncomment unused imports for now
# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# from django.contrib.auth.decorators import login_required
# from .its_system import its_request_parser_fncs_value
>>>>>>> 28b5f5cac722d1f7eb2d81c8ac0c345feb680e69

class StudentSubmissionViewSet(
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Submissiondata.objects.all()
    permission_classes = (IsStudent,)
    serializer_class = {
        "list": RetrieveAllSubmissionSerializer,
        "retrieve": RetrieveSubmissionDetailsSerializer,
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
            self.perform_create(serializer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(
                data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        
    def list(self, request):
        print('in list')
        qn_id = request.data.get('qn_id')
        # offset = request.query_params.get("offset", 0)
        # limit = request.query_params.get("limit", 10)
        queryset = self.get_queryset().filter(qn_id=qn_id)
        submissions = queryset.order_by("submission_number")
        serializer = self.get_serializer_class()(submissions, many=True)
        return Response(data={"submissions": serializer.data}, status=status.HTTP_200_OK)

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

