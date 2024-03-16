import requests
from rest_framework.exceptions import APIException

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
url = "https://its.comp.nus.edu.sg/cs3213/"


class ITSFeedbackException(APIException):
    default_detail = "Program too complex for ITS to process"


class ITSInterpreterException(APIException):
    default_detail = "Program too complex for ITS to process"


# generate parser result based on provided program
def its_request_parser(language, program):
    parser_url = url + "parser"
    data = {
        "language": language,
        "source_code": program,
    }
    response = requests.post(parser_url, headers=headers, json=data)

    if response.status_code == 200:
        # API call was successful
        return response.json()
    else:  # noqa: RET505
        # API call failed
        print(f"Error: {response.status_code}, {response.text}")
        return None


# generate interpret result based on provided program, inputs and entry functions
def its_request_interpreter(language, program_model, function, inputs, arguments):
    interpreter_url = url + "interpreter"
    data = {
        "language": language,
        "program_model": str(program_model),
        "function": function,
        "inputs": inputs,
        "args": arguments,
    }
    response = requests.post(interpreter_url, headers=headers, json=data)
    if response.status_code == 200:
        # API call was successful
        return response.json()
        # Process the JSON response as needed
    elif response.status_code == 422:  # noqa: RET505
        # API call failed
        print(f"Error: {response.status_code}, {response.text}")
        return "interpreter failed"
    else:
        raise ITSInterpreterException()


# generate JSON repair based on provided program
def its_request_feedback_fix(
    language, reference_solution, student_solution, function, inputs, arguments
):
    feedback_fix_url = url + "feedback_fix"

    data = {
        "language": language,
        "reference_solution": reference_solution,
        "student_solution": student_solution,
        "function": function,
        "inputs": inputs,
        "args": arguments,
    }
    response = requests.post(feedback_fix_url, headers=headers, json=data)
    print(response.status_code)
    if response.status_code == 200:
        # API call was successful
        return response.json()
    elif response.status_code == 422:  # noqa: RET505
        # API call failed
        print(f"Error: {response.status_code}, {response.text}")
        return "error generating feedback for tutor"
    else:
        raise ITSFeedbackException()


def its_request_feedback_hint(
    language, reference_solution, student_solution, function, inputs, arguments
):
    feedback_hint_url = url + "feedback_error"
    data = {
        "language": language,
        "reference_solution": reference_solution,
        "student_solution": student_solution,
        "function": function,
        "inputs": inputs,
        "args": arguments,
    }
    response = requests.post(feedback_hint_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 422:  # noqa: RET505
        # API call failed
        print(f"Error: {response.status_code}, {response.text}")
        return "error generating feedback hint for student"
    else:
        raise ITSFeedbackException()
