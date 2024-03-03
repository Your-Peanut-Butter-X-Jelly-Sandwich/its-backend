from rest_framework import generics, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Submissiondata
from .serializers import RetrieveSubmissionSerializer, CreateSubmissionSerializer
from django.contrib.auth.decorators import login_required

# @login_required
class SubmissionHistoryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Submissiondata.objects.all()
    serializer_class = RetrieveSubmissionSerializer
    
class CreateSubmissionView(views.APIView):
    serializer_class = CreateSubmissionSerializer

    def generate_its_feedback(self):
        # write retrival of feedback from iTS
        return "feedback from ITS"
    
    def post(self, request, qn_id):
        # if not self.request.session.exits(self.request.session.session_key):
        #     self.request.session.create()
        mutable_data = request.data.copy()
        mutable_data['qn_id'] = qn_id
        mutable_data['feedback'] = self.generate_its_feedback()
        print(mutable_data)
        serializer = self.serializer_class(data=mutable_data)

        if serializer.is_valid():
            try:
                serializer.save(qn_id=qn_id)
            except Exception as e:
                return Response(data={"message": e.args}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

