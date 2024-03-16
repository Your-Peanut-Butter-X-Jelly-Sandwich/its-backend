import json
from ast import literal_eval

from rest_framework.exceptions import APIException

from ..questions.models import Question, TestCase
from ..submissions.its_utils import ITSFeedbackException
from .its_utils import (
    its_request_feedback_fix,
    its_request_feedback_hint,
    its_request_interpreter,
    its_request_parser,
)
from .models import Submissiondata


class QuestionNotFoundError(Exception):
    pass


class CannotGeneratedFeedbackException(APIException):
    default_detail = (
        "Program too complex to cannot be processed by ITS feedback service"
    )


def get_parsed_ref_program(qn_id):
    try:
        question = Question.objects.get(pk=qn_id)
    except Question.DoesNotExist:
        raise QuestionNotFoundError(f"Question with qn_id {qn_id} not found") from None

    ref_program = question.ref_program
    language = question.language.lower()
    ref_program = ref_program.replace("\\n", "\n").replace("\\t", "\t")
    return its_request_parser(language, ref_program)


def get_parsed_stu_program(program, language):
    program = program.replace("\\n", "\n").replace("\\t", "\t")
    return its_request_parser(language, program)


def compute_score(qn_id, language, student_solution, function):
    test_cases = TestCase.objects.filter(question_id=qn_id)
    total_score = test_cases.count()
    score = 0
    failed_test_cases = []
    for test_case in test_cases:
        inputs = ""
        arguments = "[" + str(test_case.input) + "]"
        its_interpreter_response = its_request_interpreter(
            language, student_solution, function, inputs, arguments
        )
        result = its_interpreter_response["entries"][-1]["mem"]["$ret'"]
        result = str(result)
        if literal_eval(result) == literal_eval(test_case.output):
            score += 1
        else:
            failed_test_cases.append(test_case.pk)
    return total_score, score, failed_test_cases


def get_submission_number(user, qn_id):
    submissions = Submissiondata.objects.filter(submitted_by=user, qn_id=qn_id)
    return submissions.count() + 1


def get_failed_test_case_arg(failed_test_cases):
    sample_test_case = TestCase.objects.filter(pk__in=failed_test_cases)
    if sample_test_case.count() == 0:
        return ""
    else:  # noqa: RET505
        return sample_test_case.input


def process_feedback_params(
    language, parsed_ref_program, parsed_stu_program, failed_test_cases
):
    io_input = "[]"
    arguments = "[" + str(get_failed_test_case_arg(failed_test_cases)) + "]"
    language = language if language.lower() != "python" else "py"
    parsed_ref_program = json.dumps(parsed_ref_program)
    parsed_stu_program = json.dumps(parsed_stu_program)
    return io_input, arguments, language, parsed_ref_program, parsed_stu_program


def get_feedback_for_tutor(
    language, parsed_ref_program, parsed_stu_program, function, failed_test_cases
):
    io_input, arguments, language, parsed_ref_program, parsed_stu_program = (
        process_feedback_params(
            language, parsed_ref_program, parsed_stu_program, failed_test_cases
        )
    )
    try:
        feedback_fix_array = its_request_feedback_fix(
            language,
            parsed_ref_program,
            parsed_stu_program,
            function,
            io_input,
            arguments,
        )
        its_feedback_fix_tutor = {"fixes": feedback_fix_array}
        return json.dumps(its_feedback_fix_tutor)
    except ITSFeedbackException as err:
        raise CannotGeneratedFeedbackException() from err


def get_feedback_for_student(
    language, parsed_ref_program, parsed_stu_program, function, failed_test_cases
):
    io_input, arguments, language, parsed_ref_program, parsed_stu_program = (
        process_feedback_params(
            language, parsed_ref_program, parsed_stu_program, failed_test_cases
        )
    )
    try:
        feedback_hint_array = its_request_feedback_hint(
            language,
            parsed_ref_program,
            parsed_stu_program,
            function,
            io_input,
            arguments,
        )
        its_feedback_hint_student = {"hints": feedback_hint_array}
        return json.dumps(its_feedback_hint_student)
    except ITSFeedbackException as err:
        raise CannotGeneratedFeedbackException() from err


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
    total_score, score, failed_test_cases = compute_score(
        qn_id, language, parsed_stu_program, function
    )

    try:
        its_feedback_fix_tutor = get_feedback_for_tutor(
            language,
            parsed_ref_program,
            parsed_stu_program,
            function,
            failed_test_cases,
        )
    except CannotGeneratedFeedbackException:
        its_feedback_fix_tutor = {"message": ""}
        its_feedback_fix_tutor = json.dumps(its_feedback_fix_tutor)

    try:
        its_feedback_hint_student = get_feedback_for_student(
            language,
            parsed_ref_program,
            parsed_stu_program,
            function,
            failed_test_cases,
        )
    except CannotGeneratedFeedbackException:
        its_feedback_hint_student = {"message": ""}
        its_feedback_hint_student = json.dumps(its_feedback_hint_student)

    report = "no report yet"

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
