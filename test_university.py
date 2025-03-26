import sqlite3
from student import Student
conn = sqlite3.connect("university_database.db")  
cursor = conn.cursor()
from course import Course
from instructor import Instructor
# 1 | sohail_sajid | 34 | bahawalpur

# 1 | Machine Learning | DS501
# 2 | Deep Learning | DS502
# 3 | Big Data Analytics | DS503
# 5 | Natural Language Processing | DS505
# 6 | Computer Vision | DS506
# 7 | Artificial Intelligence | DS507
# 10 | Cloud Computing for Data Science | DS510

teacher=Instructor("sohail_sajid",34,"bahawalpur")
# teacher.add_course("Artificial Intelligence","DS507")
# teacher.check_students_enrolled("Artificial Intelligence","DS507")

# 1 | abubakar_idrees | 19 | gojra
# 3 | khuram_ali | 12 | kharachi
# 4 | alizeh_ilyas | 20 | bhawalpur
# 5 | taha | 21 | gojra

# teacher.assign_grades("Artificial Intelligence","DS507")
    
teacher.check_student_courses("abubakar_idrees")
teacher.check_student_courses("alizeh ilyas")
