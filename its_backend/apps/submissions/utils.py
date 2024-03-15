from .its_utils import its_request_parser_fncs_value, its_request_parser, its_request_feedback_fix
   
   
# reference solution for testing purpose:
reference_program = "def is_odd(x):\n\tif x % 2 == 0:\n\t\treturn False\n\telse:\n\t\treturn True"
reference_program_language = "py"
reference_solution = its_request_parser(reference_program_language, reference_program)
function = "is_odd"
inputs = []
args = ""

def process_submission_request(request):
    #  to generate report
        language = request.data.get('language')
        program = request.data.get('program')

        qn_id = request.data.get('qn_id')
        # referece_program
        total_score = 1
        score = 1
        submission_number = 1
        mutable_data = request.data.copy()
        student_solution = its_request_parser(language, program)
        its_feedback = [1, "no feedback yet"]
        report = its_request_feedback_fix(language, reference_solution, student_solution, function, inputs, args)

        mutable_data["qn_id"] = qn_id
        mutable_data["total_score"] = total_score
        mutable_data["score"] = score
        mutable_data["submission_number"]=submission_number
        mutable_data["its_feedback"]=its_feedback
        mutable_data["report"] = report

        print("mutable_data:",mutable_data)

        return mutable_data