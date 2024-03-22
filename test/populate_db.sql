-- Assume migrations are already made by django

-- use pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64= as password field
-- hashed form of "CS3213ITS"

-- Populate 10 students
INSERT INTO accounts_customuser (email, password, username, organisation, is_active, is_superuser, is_staff, date_joined, is_tutor, is_student, is_manager) VALUES
('stu01@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 1
('stu02@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 2
('stu03@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 3
('stu04@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 4
('stu05@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 5
('stu06@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 6
('stu07@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 7
('stu08@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 8
('stu09@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),  -- id = 9
('stu10@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0);  -- id = 10

-- Populate 5 tutors
INSERT INTO accounts_customuser (email, password, username, organisation, is_active, is_superuser, is_staff, date_joined, is_tutor, is_student, is_manager) VALUES
('tut11@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 11
('tut12@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 12
('tut13@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 13
('tut14@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 14
('tut15@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0);  -- id = 15

-- Populate 6 questions
INSERT INTO questions_question ("question_title", "question_statement", "ref_program", "language", "pub_date", "pub_by_id", "due_date") VALUES
('Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.', 'def twoSum(nums, target):
        numMap = {}
        n = len(nums)

        for i in range(n):
            complement = target - nums[i]
            if complement in numMap:
                return [numMap[complement], i]
            numMap[nums[i]] = i

        return []  # No solution found', 'python', '2024-03-16 12:44:23.804904', '11', '2024-05-13'),
('Longest Substring Without Repeating Characters', 'Given a string s, find the length of the longest substring without repeating characters.', 'def lengthOfLongestSubstring(s: str) -> int:
    n = len(s)
    maxLength = 0
    charMap = {}
    left = 0

    for right in range(n):
        if s[right] not in charMap or charMap[s[right]] < left:
            charMap[s[right]] = right
            maxLength = max(maxLength, right - left + 1)
        else:
            left = charMap[s[right]] + 1
            charMap[s[right]] = right

    return maxLength', 'python', '2024-03-16 12:45:31.519767', '11', '2024-04-06'),
('Integer to Roman', 'Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two one''s added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given an integer, convert it to a roman numeral.', 'def intToRoman(num):
    # Paso #1: Listas de valores romanos
    listado_unidad = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    listado_decena = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    listado_centena = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    listado_millar = ["", "M", "MM", "MMM"]

    # Paso #2: Obtener las unidades, decenas, centenas y millares
    millar = num // 1000
    centena = (num % 1000) // 100
    decena = (num % 100) // 10
    unidad = num % 10

    # Paso #3: Convertir cada unidad a su valor romano
    millar_romano = listado_millar[millar]
    centena_romano = listado_centena[centena]
    decena_romano = listado_decena[decena]
    unidad_romano = listado_unidad[unidad]

    # Paso #4: Concatenar las unidades para formar el número romano
    return millar_romano + centena_romano + decena_romano + unidad_romano', 'python', '2024-03-16 12:45:39.557438', '11', '2024-04-06'),
('Permutations', 'Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.', 'def permute(nums):
    def backtrack(start):
        if start == len(nums):
            permutations.append(nums[:])
        else:
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

    permutations = []
    backtrack(0)
    return permutations', 'python', '2024-03-16 12:46:15.658668', '12', '2024-04-14'),
('Standard', 'The standard test question', 'def main():
    a = 10
    b = 0
    for i in range(0, a):
        b = b + 1
    return b', 'python', '2024-03-16 12:46:26.344129', '12', '2024-04-14'),
('Is Odd', 'The standard test question', 'def is_odd(x):
	if x % 2 == 0:
		return False
	else:
		return True', 'python', '2024-03-16 12:46:26.344129', '11', '2024-04-14');

-- Pouplate 13 test cases

INSERT INTO "main"."questions_testcase" ("input", "output", "question_id") VALUES 
('[2,7,11,15],9', '[0, 1]', '1'),
('[3,2,4],6', '[1, 2]', '1'),
('[3,3],6', '[0, 1]', '1'),

('s = "abcabcbb"', '3', '2'),
('s = "bbbbb"', '1', '2'),
('s = "pwwkew"', '3', '2'),

('3', '"III"', '3'),
('58', '"LVIII"', '3'),
('1994', '"MCMXCIV"', '3'),

('[1,2,3]', '[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]', '4'),

('1', 'True', '6'),
('15', 'True', '6'),
('100', 'False', '6');

-- Populate 7 submissions
INSERT INTO submissions_submissiondata ("qn_id", "submission_number", "submission_date", "program", "status", "score", "tutor_feedback", "its_feedback_hint_student", "its_feedback_fix_tutor", "total_score", "submitted_by_id", "language") VALUES 
('1', '1', '2024-03-16 09:28:22.913025', 'def twoSum(nums, target):
	hashmap = {}
	for i in range(len(nums)):
		hashmap[nums[i]] = i
	for i in range(len(nums)):
		complement = target - nums[i]
		if complement in hashmap and hashmap[complement] != i:
			return [i, hashmap[complement]]', 'no status yet', '3', '', '""', '""', '3', '1', 'python'),
('1', '2', '2024-03-16 09:35:36.663842', 'def twoSum(nums, target):
	hashmap = {}
	for i in range(len(nums)):
		hashmap[nums[i]] = i
	for i in range(len(nums)):
		complement = target - nums[i]
		if complement in hashmap and hashmap[complement] != i:
			return [i, hashmap[complement]]', 'no status yet', '3', '', '""', '""', '3', '1', 'python'),
('1', '3', '2024-03-16 12:26:33.709593', 'def twoSum(nums, target):
	hashmap = {}
	for i in range(len(nums)):
		hashmap[nums[i]] = i
	for i in range(len(nums)):
		complement = target - nums[i]
		if complement in hashmap and hashmap[complement] != i:
			return [i, hashmap[complement]]', 'no status yet', '3', '', '"{\"message\": \"\"}"', '"{\"message\": \"\"}"', '3', '1', 'python'),
('1', '4', '2024-03-16 12:28:13.108628', 'def twoSum(nums, target):
	hashmap = {}
	for i in range(len(nums)):
		hashmap[nums[i]] = i
	for i in range(len(nums)):
		complement = target - nums[i]
		if complement in hashmap and hashmap[complement] != i:
			return [i, hashmap[complement]]', 'no status yet', '3', '', '"{\"message\": \"\"}"', '"{\"message\": \"\"}"', '3', '1', 'python'),
('3', '1', '2024-03-15 14:02:50.594625', 'def intToRoman(num: int) -> str:
	Roman = ""
	storeIntRoman = [
		[1000, "M"],
		[900, "CM"],
		[500, "D"],
		[400, "CD"],
		[100, "C"],
		[90, "XC"],
		[50, "L"],
		[40, "XL"],
		[10, "X"],
		[9, "IX"],
		[5, "V"],
		[4, "IV"],
		[1, "I"],
	]
	for i in range(len(storeIntRoman)):
		while num >= storeIntRoman[i][0]:
			Roman += storeIntRoman[i][1]
			num -= storeIntRoman[i][0]
	return Roman', 'no status yet', '0', '', '"{\"hint\": [{\"lineNumber\": 3, \"hintStrings\": [\"Incorrect else-block for if ( a > 0 )\"]}]}"', '"{\"fix\": [{\"lineNumber\": 5, \"oldExpr\": \"b = (b - 1)\", \"newExpr\": \"b = (b + 1)\", \"repairStrings\": [\"Wrong expression. Change b = (b - 1) to b = (b + 1);\"]}]}"', '3', '1', 'python'),
('3', '2', '2024-03-15 14:15:29.379233', 'def intToRoman(num: int) -> str:
	Roman = ""
	storeIntRoman = [
		[1000, "M"],
		[900, "CM"],
		[500, "D"],
		[400, "CD"],
		[100, "C"],
		[90, "XC"],
		[50, "L"],
		[40, "XL"],
		[10, "X"],
		[9, "IX"],
		[5, "V"],
		[4, "IV"],
		[1, "I"],
	]
	for i in range(len(storeIntRoman)):
		while num >= storeIntRoman[i][0]:
			Roman += storeIntRoman[i][1]
			num -= storeIntRoman[i][0]
	return Roman', 'no status yet', '0', '', '"{\"hint\": [{\"lineNumber\": 3, \"hintStrings\": [\"Incorrect else-block for if ( a > 0 )\"]}]}"', '"{\"fix\": [{\"lineNumber\": 5, \"oldExpr\": \"b = (b - 1)\", \"newExpr\": \"b = (b + 1)\", \"repairStrings\": [\"Wrong expression. Change b = (b - 1) to b = (b + 1);\"]}]}"', '3', '1', 'python'),
('3', '3', '2024-03-15 14:16:40.151735', 'def intToRoman(num: int) -> str:
	Roman = ""
	storeIntRoman = [
		[1000, "M"],
		[900, "CM"],
		[500, "D"],
		[400, "CD"],
		[100, "C"],
		[90, "XC"],
		[50, "L"],
		[40, "XL"],
		[10, "X"],
		[9, "IX"],
		[5, "V"],
		[4, "IV"],
		[1, "I"],
	]
	for i in range(len(storeIntRoman)):
		while num >= storeIntRoman[i][0]:
			Roman += storeIntRoman[i][1]
			num -= storeIntRoman[i][0]
	return Roman', 'no stau yet', '3', '', '"{\"hint\": [{\"lineNumber\": 3, \"hintStrings\": [\"Incorrect else-block for if ( a > 0 )\"]}]}"', '"{\"fix\": [{\"lineNumber\": 5, \"oldExpr\": \"b = (b - 1)\", \"newExpr\": \"b = (b + 1)\", \"repairStrings\": [\"Wrong expression. Change b = (b - 1) to b = (b + 1);\"]}]}"', '3', '1', 'python');
