-- Assume migrations are already made by django

-- use pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64= as password field
-- hashed form of "CS3213ITS"

-- Populate 10 students
INSERT INTO accounts_customuser (email, password, username, organisation, is_active, is_superuser, is_staff, date_joined, is_tutor, is_student, is_manager) VALUES
('stu01@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 1
('stu02@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 2
('stu03@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 3
('stu04@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 4
('stu05@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 5
('stu06@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 6
('stu07@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 7
('stu08@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 8
('stu09@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0),      -- id = 9
('stu10@student.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 0, 1, 0);      -- id = 10

-- Populate 5 tutors
INSERT INTO accounts_customuser (email, password, username, organisation, is_active, is_superuser, is_staff, date_joined, is_tutor, is_student, is_manager) VALUES
('tut11@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 11
('tut12@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 12
('tut13@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 13
('tut14@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0),  -- id = 14
('tut15@tutor.com', 'pbkdf2_sha256$720000$cp2TzSkZWwFe6Ztj8zU0cu$RnmYUQ1IX7Nr3gZtyvW42sGJNHBHOWttpyUhsZKCE64=', '', '', 1, 0, 0, CURRENT_DATE, 1, 0, 0);  -- id = 15
