from .its_utils import its_request_interpreter, its_request_parser, its_request_feedback_fix
from ..questions.models import Question, TestCase   
from .models import Submissiondata

class QuestionNotFoundException(Exception):
    pass

def process_submission_request(request):
        language = request.data.get('language')
        program = request.data.get('program')
        qn_id = request.data.get('qn_id')

        # get testcases and ref_program from question DB
        try:
            question = Question.objects.get(pk=qn_id)
        except Question.DoesNotExist:
            raise QuestionNotFoundException(f"Question with qn_id {qn_id} not found")
        
        ref_program = question.ref_program
        mutable_data = request.data.copy()
        program = program.replace("\\n", "\n").replace("\\t", "\t")    
        
        test_cases = TestCase.objects.filter(question_id=qn_id)
        total_score = test_cases.count()

        # interpretate all the test cases
        student_solution = its_request_parser(language, program)
        function = next(iter(student_solution['fncs'].keys()))
        score = 0
        for test_case in test_cases:
            inputs = ""
            args = "[" + str(test_case.input) + "]"
            its_interpreter_response = its_request_interpreter(language, student_solution, function, inputs, args)
            result = its_interpreter_response['entries'][0]['mem']["$ret'"]
            # print("result  ", result, type(result),"actual output: ", test_case.output, type(test_case.output))
            if str(result) == test_case.output:
                score += 1

        its_feedback = [1, "no feedback yet"]
        inputs = ''
        args = ''
        report = its_request_feedback_fix(language, ref_program, student_solution, function, inputs, args)

        # generate report

        # get submission number
        submissions = Submissiondata.objects.filter(submitted_by=request.user, qn_id=qn_id)
        submission_number = submissions.count() + 1

        # reform the request data
        mutable_data["qn_id"] = qn_id
        mutable_data["total_score"] = total_score
        mutable_data["score"] = score
        mutable_data["submission_number"]=submission_number
        mutable_data["its_feedback"]=its_feedback
        mutable_data["report"] = report

        print("mutable_data:",mutable_data)

        return mutable_data
