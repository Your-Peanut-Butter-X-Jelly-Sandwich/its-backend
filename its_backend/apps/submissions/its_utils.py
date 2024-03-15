

import requests
import json


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
url = 'https://its.comp.nus.edu.sg/cs3213/'

# generate parser result based on provided program
def its_request_parser(language, program):
    parser_url = url + 'parser'

    data = {
        'language': language,
        'source_code': program,
    }
    print(data)
    response = requests.post(parser_url, headers=headers, json=data)

    if response.status_code == 200:
        # API call was successful
        json_response = response.json()
        # Access the 'fncs' field from the JSON response
        fncs_value = json_response.get('fncs')
        # print(json_response)
        return json_response
    else:
        # API call failed
        print(f'Error: {response.status_code}, {response.text}')
        return None
    

def its_request_parser_fncs_value(language, source_code):
    json_response = its_request_parser(language, source_code)
    return json_response.get('fncs')

# generate interpret result based on provided program, inputs and entry functions
def its_request_interpreter(language, program_model, function, inputs, args):
    interpreter_url = url + 'interpreter'
    data = {
        "language": language,
        "program_model": str(program_model),
        "function": function,
        "inputs": inputs,
        "args": args
    }
    response = requests.post(interpreter_url, headers=headers, json=data)

    if response.status_code == 200:
        # API call was successful
        json_response = response.json()
        # Process the JSON response as needed
        return json_response
    else:
        # API call failed
        print(f'Error: {response.status_code}, {response.text}')


# generate JSON repair based on provided program
def its_request_feedback_fix(language, reference_solution, student_solution, function, inputs, args):
    feedback_fix_url = url + 'feedback_fix'

    data = {
        "language": language,
        "reference_solution": reference_solution,
        "student_solution": student_solution,
        "function": function,
        "inputs": inputs,
        "args": args
    }

    response = requests.post(feedback_fix_url, headers=headers, json=data)

    if response.status_code == 200:
        # API call was successful
        json_response = response.json()
        # Process the JSON response as needed
        # print(json_response)
        repair_strings = data[0]['repairStrings']
        return repair_strings
    else:
        # API call failed
        print(f'Error: {response.status_code}, {response.text}')
        return "error generating Feedback"










