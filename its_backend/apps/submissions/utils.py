from .its_utils import (
    its_request_interpreter,
    its_request_parser,
    its_request_feedback_fix,
)
from ..questions.models import Question, TestCase
from .models import Submissiondata
import json


class QuestionNotFoundException(Exception):
    pass


def process_submission_request(request):
    language = request.data.get("language")
    program = request.data.get("program")
    qn_id = request.data.get("qn_id")
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
    function = next(iter(student_solution["fncs"].keys()))
    score = 0
    for test_case in test_cases:
        inputs = ""
        args = "[" + str(test_case.input) + "]"
        its_interpreter_response = its_request_interpreter(
            language, student_solution, function, inputs, args
        )
        result = its_interpreter_response["entries"][-1]["mem"]["$ret'"]
        # print("result  ", result, type(result),"actual output: ", test_case.output, type(test_case.output))
        result = '"' + str(result) + '"'
        if result == test_case.output:
            score += 1

    its_feedback_fix_tutor = {
        "fix": [
            {
                "lineNumber": 5,
                "oldExpr": "b = (b - 1)",
                "newExpr": "b = (b + 1)",
                "repairStrings": [
                    "Wrong expression. Change b = (b - 1) to b = (b + 1);"
                ],
            }
        ]
    }
    its_feedback_hint_student = {
        "hint": [
            {"lineNumber": 3, "hintStrings": ["Incorrect else-block for if ( a > 0 )"]}
        ]
    }
    inputs = "[]"
    args = ""
    its_feedback_fix_tutor = json.dumps(its_feedback_fix_tutor)
    its_feedback_hint_student = json.dumps(its_feedback_hint_student)
    print(1111111111, type(its_feedback_fix_tutor))

    parsed_ref_program = its_request_parser(language, ref_program)

    # feedback_fix = its_request_feedback_fix(language, parsed_ref_program, student_solution, function, inputs, args)
    # print("feedback_fix", feedback_fix)
    # generate report?? if there is
    report = " no report yet"

    # get submission number
    submissions = Submissiondata.objects.filter(submitted_by=request.user, qn_id=qn_id)
    submission_number = submissions.count() + 1

    # reform the request data
    mutable_data["qn_id"] = qn_id
    mutable_data["total_score"] = total_score
    mutable_data["score"] = score
    mutable_data["submission_number"] = submission_number
    mutable_data["its_feedback_hint_student"] = its_feedback_hint_student
    mutable_data["its_feedback_fix_tutor"] = its_feedback_fix_tutor

    mutable_data["report"] = report

    print("mutable_data:", mutable_data)

    return mutable_data
