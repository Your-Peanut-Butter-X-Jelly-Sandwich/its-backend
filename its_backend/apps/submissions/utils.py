from .its_utils import (
    its_request_interpreter,
    its_request_parser,
    its_request_feedback_fix,
    its_request_feedback_hint,
)
from ..questions.models import Question, TestCase
from .models import Submissiondata
import json


class QuestionNotFoundException(Exception):
    pass


def get_parsed_ref_program(qn_id):
    try:
        question = Question.objects.get(pk=qn_id)
    except Question.DoesNotExist:
        raise QuestionNotFoundException(f"Question with qn_id {qn_id} not found")

    ref_program = question.ref_program
    language = question.language.lower()
    parsed_ref_program = its_request_parser(language, ref_program)
    return parsed_ref_program


def get_parsed_stu_program(program, language):
    program = program.replace("\\n", "\n").replace("\\t", "\t")
    parsed_stu_program = its_request_parser(language, program)
    return parsed_stu_program


def compute_score(qn_id, language, student_solution, function):
    test_cases = TestCase.objects.filter(question_id=qn_id)
    total_score = test_cases.count()
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
    return total_score, score


def get_submission_number(user, qn_id):
    submissions = Submissiondata.objects.filter(submitted_by=user, qn_id=qn_id)
    submission_number = submissions.count() + 1
    return submission_number


def get_feedback_for_tutor(language, parsed_ref_program, parsed_stu_program, function):
    input = "[]"
    args = ""
    language = language if language.lower() != "python" else "py"
    parsed_ref_program = json.dumps(parsed_ref_program)
    parsed_stu_program = json.dumps(parsed_stu_program)
    feedback_fix_array = its_request_feedback_fix(
        language, parsed_ref_program, parsed_stu_program, function, input, args
    )
    its_feedback_fix_tutor = {"fixes": feedback_fix_array}
    return json.dumps(its_feedback_fix_tutor)


def get_feedback_for_student(
    language, parsed_ref_program, parsed_stu_program, function
):
    input = "[]"
    args = ""
    language = language if language.lower() != "python" else "py"
    parsed_ref_program = json.dumps(parsed_ref_program)
    parsed_stu_program = json.dumps(parsed_stu_program)
    feedback_hint_array = its_request_feedback_hint(
        language, parsed_ref_program, parsed_stu_program, function, input, args
    )
    its_feedback_hint_student = {"hints": feedback_hint_array}
    return json.dumps(its_feedback_hint_student)


def generate_report():
    pass


def process_submission_request(request):
    language = request.data.get("language")
    program = request.data.get("program")
    qn_id = request.data.get("qn_id")

    mutable_data = request.data.copy()

    # parsed student and reference program
    parsed_stu_program = get_parsed_stu_program(program, language)
    parsed_ref_program = get_parsed_ref_program(qn_id)

    # the entry function of the program
    function = next(iter(parsed_stu_program["fncs"].keys()))

    # number of test cases passed
    total_score, score = compute_score(qn_id, language, parsed_stu_program, function)

    its_feedback_fix_tutor = get_feedback_for_tutor(
        language, parsed_ref_program, parsed_stu_program, function
    )
    its_feedback_hint_student = get_feedback_for_student(
        language, parsed_ref_program, parsed_stu_program, function
    )

    # feedback_fix = its_request_feedback_fix(language, parsed_ref_program, student_solution, function, inputs, args)
    # print("feedback_fix", feedback_fix)
    # generate report?? if there is
    report = " no report yet"

    # get submission number
    submission_number = get_submission_number(request.user, qn_id)

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
