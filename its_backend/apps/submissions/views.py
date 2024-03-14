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

# reference solution for testing purpose:
reference_program = "def is_odd(x):\n\tif x % 2 == 0:\n\t\treturn False\n\telse:\n\t\treturn True"
reference_program_language = "py"
reference_solution = its_request_parser(reference_program_language, reference_program)
function = "is_odd"
inputs = []
args = ""

# @login_required
class SubmissionHistoryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Submissiondata.objects.all()
    serializer_class = RetrieveSubmissionSerializer
    
# @login_required
class CreateSubmissionView(views.APIView):
    serializer_class = CreateSubmissionSerializer

    def post(self, request, qn_id):
        language = request.data.get('language')
        program = request.data.get('program')
        mutable_data = request.data.copy()
        student_solution = its_request_parser(language, program)
        report = its_request_feedback_fix(language, reference_solution, student_solution, function, inputs, args)

        mutable_data['qn_id'] = qn_id
        mutable_data['program'] = program
        mutable_data['report'] = report
        serializer = self.serializer_class(data=mutable_data)

        if serializer.is_valid():
            try:
                serializer.save(qn_id=qn_id, program=program, report=report)
            except Exception as e:
                return Response(data={"message": e.args}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

