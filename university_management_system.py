from student import Student
from instructor import Instructor
from course import Course
import sqlite3

#start
class University:
    def __init__(self): 
        while(True):
            print("\n***Welcome to University Portal***")
            print(" 1-Admin Panel")
            print(" 2-Instructor Panel")
            print(" 3-Student Panel")
            print(" 4-Exit")
            try:
                option=int(input("Enter the option here: "))
            except:
                option=-1
            match option:
#admin panel
                    case 1:
                        while(True):
                            print("\nWelcome Admin")
                            print(" 1-Student Section")
                            print(" 2-Instructor Section")
                            print(" 3-Course Section")
                            print(" 4-Return to main menu")                         
                            try:
                                option=int(input("Enter the option here: "))
                            except:
                                option=-1
                            match option:
                                #ADMIN-STUDENT
                                case 1:
                                    while(True):
                                        print("\nStudent section: ")
                                        print(" 1-ADD Student")
                                        print(" 2-REMOVE Student")
                                        print(" 3-UPDATE Student")
                                        print(" 4-SEE Student LIST")
                                        print(" 5-Return")
                                        try:
                                            option=int(input("Enter the option here: "))
                                        except:
                                            option=-1
                                        match option:
                                            case 1:
                                                print("\nAdding student")
                                                name=input("Enter Student name: ")
                                                while(True):
                                                    try:
                                                        age=int(input("Enter Student age: "))
                                                        if age>0:
                                                            break
                                                    except:
                                                        print("Invalid age")
                                                
                                                city=input("Enter Studente city: ")
                                                new_student=Student(name,age,city)
                                                new_student.add_student()
 
                                            case 2:
                                                print("\nRemove student")
                                                name=input("Enter the name of student: ")
                                                name="_".join(name.split()).lower()
                                                new_student=Student("temp",12,"temp")
                                                new_student.remove_student(name)                                              
 
                                            case 3:
                                                print("\nUpdate Student data")
                                                name=input("Enter the name of Student: ")
                                                name="_".join(name.split()).lower()
                                                conn = sqlite3.connect("university_database.db")
                                                cursor = conn.cursor()
                                                cursor.execute("SELECT name FROM student;")
                                                students = cursor.fetchall()
                                                found=False    
                                                for student in students:
                                                    if student[0]==name:
                                                        found=True
                                                if found==False:
                                                    print("Student not found!")
                                                    
                                                    conn.close() 
                                                while found:
                                                    print("\nWhat do you want to edit")
                                                    print(" 1-Name")
                                                    print(" 2-age")
                                                    print(" 3-city")
                                                    print(" 4-return")
                                                    new_student=Student("temp",12,"temp")
                                                    try:
                                                        option=int(input("Enter the option here: "))
                                                    except:
                                                        option=-1
                                                    match option:
                                                        case 1:
                                                            print("\nUpdate name:")
                                                            new_name=input("Enter the student name (new): ")
                                                            new_name="_".join(new_name.split()).lower()
                                                            new_student.update_name(name,new_name)
                                                        
                                                        case 2:
                                                            print("\nUpdate age ")
                                                            while(True):
                                                                try:
                                                                    age=int(input("Enter Student age: "))
                                                                    if age>0:
                                                                        break
                                                                except:
                                                                    print("Invalid age")
                                                            new_student.update_age(name,age)
                                                        case 3:
                                                            print("Update City")
                                                            new_city=input("Enter the city name (new): ")
                                                            new_student.update_city(name,new_city)

                                                        case 4:
                                                            print("returing")
                                                            break
                                                        
                                                        case _:
                                                            print("Ivalid choice")

                                            case 4:
                                                print("\nAll students List")
                                                new_student=Student("temp",1,"temp")
                                                new_student.list_of_students()

                                            case 5:
                                                print("returing..")
                                                break

                                            case _:
                                                print("Invalid choice!")
                               #ADMIN-Instructor
                                case 2:
                                    while(True):
                                        print("\nInstructor section: ")
                                        print(" 1-ADD Instructor")
                                        print(" 2-REMOVE Instructor")
                                        print(" 3-UPDATE Instructor")
                                        print(" 4-SEE Instructor LIST")
                                        print(" 5-Return")
                                        try:
                                            option=int(input("Enter the option here: "))
                                        except:
                                            option=-1
                                        match option:
                                            case 1:
                                                print("\nAdding instructor")
                                                name=input("Enter instructor name: ")
                                                while(True):
                                                    try:
                                                        age=int(input("Enter instructor age: "))
                                                        if age>0:
                                                            break
                                                    except:
                                                        print("Invalid age")
                                                
                                                city=input("Enter instructor city: ")
                                                instructor=Instructor(name,age,city)
                                                instructor.add_instructor()
                                            case 2:
                                                print("\nRemove Instructor")
                                                name=input("Enter the name of Instructor: ")
                                                name="_".join(name.split()).lower()
                                                new_instructor=Instructor("temp",12,"temp")
                                                new_instructor.remove_instructor(name)
                                                
                                            case 3:
                                                print("\nUpdate instructor data")
                                                name=input("Enter the name of instructor: ")
                                                name="_".join(name.split()).lower()
                                                conn = sqlite3.connect("university_database.db")
                                                cursor = conn.cursor()
                                                cursor.execute("SELECT name FROM instructor;")
                                                instructors = cursor.fetchall()
                                                found=False    
                                                for instructor in instructors:
                                                    if instructor[0]==name:
                                                        found=True
                                                    
                                                if found==False:
                                                    print("Instuctor not found!")
                                                    
                                                    conn.close() 
                                                while found:
                                                    print("\nWhat do you want to edit")
                                                    print(" 1-Name")
                                                    print(" 2-age")
                                                    print(" 3-city")
                                                    print(" 4-return")
                                                    new_instructor=Instructor("temp",12,"temp")
                                                    try:
                                                        option=int(input("Enter the option here: "))
                                                    except:
                                                        option=-1
                                                    match option:
                                                        case 1:
                                                            print("\nUpdate name:")
                                                            new_name=input("Enter the instructor name (new): ")
                                                            new_name="_".join(new_name.split()).lower()
                                                            new_instructor.update_name(name,new_name)
                                                        
                                                        case 2:
                                                            print("\nUpdate age ")
                                                            while(True):
                                                                try:
                                                                    age=int(input("Enter instructor age: "))
                                                                    if age>0:
                                                                        break
                                                                except:
                                                                    print("Invalid age")
                                                            new_instructor.update_age(name,age)
                                                        case 3:
                                                            print("Update City")
                                                            new_city=input("Enter the city name (new): ")
                                                            new_instructor.update_city(name,new_city)

                                                        case 4:
                                                            print("returing")
                                                            break
                                                        
                                                        case _:
                                                            print("Ivalid choice")

                                            case 4:
                                                print("\nAll instructor List")
                                                new_instructor=Instructor("temp",1,"temp")
                                                new_instructor.list_of_instructors()
                                            
                                            case 5:
                                                print("returing..")
                                                break
                                            case _:
                                                print("Invalid choice!")
                                #ADMIN-Course
                                case 3:
                                    while(True):
                                        print("\nCourse section: ")
                                        print(" 1-ADD Course")
                                        print(" 2-REMOVE Course")
                                        print(" 3-SEE Course LIST")
                                        print(" 4-Return")
                                        try:
                                            option=int(input("Enter the option here: "))
                                        except:
                                            option=-1
                                        match option:
                                            case 1:
                                                print("\nAdding Course")
                                                course_name=input("Enter the course name: ").title()
                                                course_code=input("Enter the course code: ").capitalize()
                                                new_course=Course(course_name,course_code)
                                                new_course.add_course_in_list()
                                            case 2:
                                                print("Removing course")
                                                course_name=input("Enter the course name: ").title()
                                                delete_course=Course("temp","Temp")
                                                delete_course.delete_course(course_name)
                                            case 3:
                                                print("List of  course")
                                                show_course=Course("temp","Temp")
                                                show_course.show_courses()
                                            case 4:
                                                print("returing..")
                                                break
                                            case _:
                                                print("Invalid choice")





                                

                                case 4:
                                    print("Return to main menu...")
                                    break
                                
                                case _:
                                    print("Invalid choice")
#instructor panel                   
                    case 2:  
                        while(True):
                            print("\nWelcome Instructor") 
                            print(" 1-Add Course")
                            print(" 2-remove Course")
                            print(" 3-Show Course")
                            print(" 4-Show student list for a specific course") 
                            print(" 5-Assign Grades") 
                            print(" 6-Update Grades")
                            print(" 7-Exit")
                            try:
                                option=int(input("Enter the option here: "))
                            except:
                                option=-1
                            match option:
                                case 1:
                                    print("\nAdd cousre")
                                    instructor_name=input("Enter the name of Instructor: ")
                                    instructor_name="_".join(instructor_name.split()).lower()
                                    teacher=Instructor(instructor_name,1,"temp")
                                    course_name=input("Enter the course name: ").title()
                                    course_code=input("Enter the course code: ").upper()
                                    teacher.add_course(course_name,course_code)
                                case 2:
                                    print("\nremoving cousre")
                                    instructor_name=input("Enter the name of Instructor: ")
                                    instructor_name="_".join(instructor_name.split()).lower()
                                    teacher=Instructor(instructor_name,1,"temp")
                                    course_name=input("Enter the course name: ").title()
                                    course_code=input("Enter the course code: ").upper()
                                    teacher.remove_course_from_instructor(instructor_name,course_name,course_code)
                                case 3:
                                    print("\nshow courses")
                                    instructor_name=input("Enter the name of Instructor: ")
                                    instructor_name="_".join(instructor_name.split()).lower()
                                    teacher=Instructor(instructor_name,1,"temp")
                                    teacher.show_enrolled_courses()
                                case 4:
                                    print("\nCheck student enroled in a course")
                                    teacher=Instructor("temp",1,"temp")
                                    course_name=input("Enter the course name: ").title()
                                    course_code=input("Enter the course code: ").upper()
                                    teacher.check_students_enrolled(course_name,course_code)
                                case 5:
                                    print("\nAssign grade")
                                    teacher=Instructor("temp",1,"temp")
                                    course_name=input("Enter the course name: ").title()
                                    course_code=input("Enter the course code: ").upper()
                                    teacher.assign_grades(course_name,course_code)

                                case 6:
                                    print("\nUpdate grade")
                                    student_name=input("Enter name of student: ")
                                    student_name="_".join(student_name.split()).lower()
                                    course_name=input("Enter the course name: ").title()
                                    course_code=input("Enter the course code: ").upper()
                                    new_grade=input("Enter the new grade: ").upper()
                                    teacher=Instructor("temp",1,"temp")
                                    teacher.update_student_grade(student_name,course_name,course_code,new_grade)

                                case 7:
                                    print("\nExiting")
                                    break
                                case _:
                                    print("\ninvalid choice")
#student panel
                    case 3:
                        student_name=input("please enter name: ")
                        student_name="_".join(student_name.split()).lower()
                        info_student=Student(student_name,1,"temp") 
                        while True:
                            print("\nWelcome Student")
                            print(" 1-Add course") 
                            print(" 2-remove course") 
                            print(" 3-show courses") 
                            print(" 4-show cgp") 
                            print(" 5-Exit") 
                            try:
                                option=int(input("Enter the option here: "))
                            except:
                                option=-1
                            match option:
                                case 1:
                                    print("\nAdd course")
                                    course_name=input("Enter the course name: ").title()
                                    course_code=input("Enter the course code: ").upper()
                                case 2:
                                    print("\nremove course")
                                    course_name=input("Enter the course name: ").title()
                                    info_student.add_course(course_name)
                                case 3:
                                    print("\nShow courses")
                                    info_student.enrolled_course()
                                case 4 :
                                    print("\nCurrent cgp")
                                    info_student.calculate_student_cgpa(student_name)
                                case 5:
                                    print("Returing to main menu")
                                    break
                                case _:
                                    print("Invalid choice")

                    case 4:
                        print("Exiting...")
                        break

                    case _:
                        print("Invalid option")


University() 