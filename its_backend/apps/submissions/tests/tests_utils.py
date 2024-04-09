from django.core.management import call_command
from django.test import TestCase

from ..utils import process_submission


class SubmissionUtilsTest(TestCase):
    def setUp(self):
        question_fixture_file_path = 'its_backend/apps/fixtures/questions_fixture.json'
        accounts_fixture_file_path = 'its_backend/apps/fixtures/accounts_fixture.json'
        
        # Load the fixture data into the database
        call_command('loaddata', accounts_fixture_file_path, verbosity=0)
        call_command('loaddata', question_fixture_file_path, verbosity=0)
        
    def test_process_submission_1_all_testcases_passed(self):
        qn_id = 1
        language = "python"
        program =  "def twoSum(nums, target):\n        numMap = {}\n        n = len(nums)\n        for i in range(n):\n            complement = target - nums[i]\n            if complement in numMap:\n                return [numMap[complement], i]\n            numMap[nums[i]] = i\n        return [] "
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 1, 'total_score': 3, 'score': 3, 'its_feedback_hint_student': '{"hints": []}', 'its_feedback_fix_tutor': '{"fixes": []}', 'status': 'ITS SUCCESS'}
        self.assertEqual(result, expected_output)

    def test_process_submission_2_some_testcases_failed(self):
        qn_id = 8
        language = "python"
        program =  "def is_odd(x):\n\tif x % 2 == 0:\n\t\treturn False\n\telse:\n\t\treturn False"  
        result = process_submission(qn_id, language, program)
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 8, 'total_score': 4, 'score': 2, 'its_feedback_hint_student': '{"hints": [{"lineNumber": 2, "hintStrings": ["Incorrect else block for if( ((x % 2) == 0) )"]}]}', 'its_feedback_fix_tutor': '{"fixes": [{"lineNumber": 2, "oldExpr": "{return False; }", "newExpr": "{ return True; }", "repairStrings": ["You need to change the condition/body of if-conditions", "Change the else-body of if(((x % 2) == 0)) to { return True; }"]}]}', 'status': 'ITS SUCCESS'}
        self.assertEqual(result, expected_output)

    def test_process_submission_3_all_testcases_failed(self):
        qn_id = 8
        language = "python"
        program =  "def is_odd(x):"
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 8, 'total_score': 4, 'score': 0, 'its_feedback_hint_student': '{"hints": [{"lineNumber": 1, "hintStrings": ["You need to add 1 or more if-conditions", "Consider conditions if (((x % 2) == 0))"]}]}', 'its_feedback_fix_tutor': '{"fixes": [{"lineNumber": 1, "oldExpr": "", "newExpr": "(((x % 2) == 0)) { return False; } else { return True; }", "repairStrings": ["You need to add 1 or more if-conditions", "Add if (((x % 2) == 0)) { return False; } else { return True; }"]}]}', 'status': 'ITS SUCCESS'}
        self.assertEqual(result, expected_output)
    
    def test_process_submission_4_its_parser_generates_empty_result(self):
        qn_id = 1
        language = "python"
        program = "d"
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 1, 'total_score': 3, 'score': 0, 'its_feedback_hint_student': '{"hints": []}', 'its_feedback_fix_tutor': '{"fixes": []}', 'status': 'The ITS parser generates empty parsed result for the Student Submission Program. '}
        self.assertEqual(result, expected_output)

    def test_process_submission_5_its_failed_in_parsing_student_program(self):
        qn_id = 1
        language = "python"
        program = "        numMap = {}\n        n = len(nums)\n        for i in range(n):\n            complement = target - nums[i]\n            if complement in numMap:\n                return [numMap[complement], i]\n            numMap[nums[i]] = i\n        return [] "
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 1, 'total_score': 3, 'score': 0, 'its_feedback_hint_student': '{"hints": []}', 'its_feedback_fix_tutor': '{"fixes": []}', 'status': 'The ITS failed to parse Student Program and raises 500 Internal Error. '}
        self.assertEqual(result, expected_output)

    def test_process_submission_6_its_failed_in_parsing_reference_program(self):
        qn_id = 3
        language = "python"
        program =  "def intToRoman(num):\n    listado_unidad = [\"\", \"I\", \"II\", \"III\", \"IV\", \"V\", \"VI\", \"VII\", \"VIII\", \"IX\"]\n    listado_decena = [\"\", \"X\", \"XX\", \"XXX\", \"XL\", \"L\", \"LX\", \"LXX\", \"LXXX\", \"XC\"]\n    listado_centena = [\"\", \"C\", \"CC\", \"CCC\", \"CD\", \"D\", \"DC\", \"DCC\", \"DCCC\", \"CM\"]\n    listado_millar = [\"\", \"M\", \"MM\", \"MMM\"]\n\n    millar = num // 1000\n    centena = (num % 1000) // 100\n    decena = (num % 100) // 10\n    unidad = num % 10\n\n    millar_romano = listado_millar[millar]\n    centena_romano = listado_centena[centena]\n    decena_romano = listado_decena[decena]\n    unidad_romano = listado_unidad[unidad]\n\n    return millar_romano + centena_romano + decena_romano + unidad_romano"
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 3, 'total_score': 3, 'score': 0, 'its_feedback_hint_student': '{"hints": []}', 'its_feedback_fix_tutor': '{"fixes": []}', 'status': 'The ITS failed to parse Reference Program and raises 500 Internal Error. '}
        self.assertEqual(result, expected_output)

    def test_process_submission_7_its_failed_in_interpreter(self):
        qn_id = 2
        language = "python"
        program = "def lengthOfLongestSubstring(s: str) -> int:\n    n = len(s)\n    maxLength = 0\n    charMap = {}\n    left = 0\n\n    for right in range(n):\n        if s[right] not in charMap or charMap[s[right]] < left:\n            charMap[s[right]] = right\n            maxLength = max(maxLength, right - left + 1)\n        else:\n            left = charMap[s[right]] + 1\n            charMap[s[right]] = right\n\n    return maxLength"
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 2, 'total_score': 0, 'score': 0, 'its_feedback_hint_student': '{"hints": []}', 'its_feedback_fix_tutor': '{"fixes": []}', 'status': 'The ITS interpreter fails to interprete the Program and Testcases. The ITS fails to provide Feedback Fix. The ITS fails to provide Feedback Hint. '}
        self.assertEqual(result, expected_output)   

    def test_process_submission_8_its_failed_in_feedback_generation(self):
        qn_id = 1
        language = "python"
        program = "def twoSum(nums, target):\n        numMap = {}\n        n = len(nums)\n        for i in range(n - 1):\n            complement = target - nums[i]\n            if complement in numMap:\n                return [numMap[complement], i]\n            numMap[nums[i]] = i\n        return [] "
        result = process_submission(qn_id, language, program)
        expected_output = {'qn_id': 1, 'total_score': 3, 'score': 1, 'its_feedback_hint_student': '{"hints": []}', 'its_feedback_fix_tutor': '{"fixes": []}', 'status': 'The ITS fails to provide Feedback Fix. The ITS fails to provide Feedback Hint. '}
        self.assertEqual(result, expected_output)      