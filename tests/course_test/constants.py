role_teacher = "Преподаватель"
role_teacher_id = 1
role_student = "Студент"
role_student_id = 2

email_student = "student@mail.ru"
password_student = "qwerty"
id_student = 1


email_teacher = "teacher@mail.ru"
password_teacher = "qwerty"
id_teacher = 2


name_course = "Математика"
description_course = "Базовая математика"
id_course = 1

name_test = "Математика тест 1"
limit = 3600
id_test = 1

questions = [
    {"text_question": "1 + 1", "options": ["1", "2", "3"], "correct_answer": "2"}
]
deadline_date = 1737950101

result_test = [
    {
        "text_question": "1 + 1",
        "options": ["1", "2", "3"],
        "correct_answer": "2",
        "student_answer": "2",
    }
]

count_current_answer = sum(
    1 for item in result_test if item["correct_answer"] == item["student_answer"]
)
