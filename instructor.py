from person import Person 

import sqlite3  
conn = sqlite3.connect("university_database.db")  
cursor = conn.cursor()


class Instructor(Person): 
    def __init__(self, name, age, city):  
        super().__init__(name, age, city)  
        self.create_instructor_table()

    def create_instructor_table(self):

        cursor.execute("""  
            CREATE TABLE IF NOT EXISTS instructor (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                name TEXT UNIQUE,  
                age INTEGER NOT NULL,  
                city TEXT NOT NULL  
            )  
        """)  
        conn.commit()

    def add_instructor(self):

        try:
            cursor.execute("INSERT INTO instructor (name, age, city) VALUES (?, ?, ?)",  
                           (self.name, self.age, self.city))  
            conn.commit()
            print(f"✅ {self.name} ADDED as an instructor.")  

            # Create personal courses table for instructor
            cursor.execute(f"""  
                CREATE TABLE IF NOT EXISTS "{self.name}_courses" (  
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    course_name TEXT UNIQUE,  
                    course_code TEXT NOT NULL  
                )  
            """)  
            conn.commit()

        except sqlite3.IntegrityError:  
            print(f"⚠️ {self.name} already exists as an instructor.")

    def remove_instructor(self, name):
      
        try:
            # Delete instructor's course table
            cursor.execute(f'DROP TABLE IF EXISTS "{name}_courses"')

            # Delete instructor from the main instructor table
            cursor.execute("DELETE FROM instructor WHERE name = ?", (name,))
            
            conn.commit()
            print(f"✅ Instructor '{name}' and their courses have been removed.")

        except sqlite3.Error as e:
            print(f"❌ Error: {e}")

    def list_of_instructors(self):  
       
        cursor.execute("SELECT * FROM instructor")  
        rows = cursor.fetchall()  

        if not rows:  
            print("⚠️ No instructors found in the database.")  
            return  

        # Get column names dynamically  
        cursor.execute("PRAGMA table_info(instructor)")  
        columns = [col[1] for col in cursor.fetchall()]  
        print(" | ".join(columns))  

        # Print instructor data  
        for row in rows:  
            print(" | ".join(str(value) for value in row)) 
    
    def update_name(self, old_name, new_name):
        """Updates the instructor's name and renames their courses table."""
        try:
            cursor.execute("SELECT name FROM instructor WHERE name = ?", (old_name,))
            if not cursor.fetchone():
                print(f"⚠️ Instructor '{old_name}' not found.")
                return
            
            cursor.execute("UPDATE instructor SET name = ? WHERE name = ?", (new_name, old_name))  
            cursor.execute(f'ALTER TABLE "{old_name}_courses" RENAME TO "{new_name}_courses"')  
            conn.commit()
            print(f"✅ Instructor name updated from '{old_name}' to '{new_name}'.")  

        except sqlite3.Error as e:
            print(f"❌ Error updating name: {e}")

    def update_age(self, name, new_age):
        """Updates the instructor's age."""
        try:
            cursor.execute("SELECT name FROM instructor WHERE name = ?", (name,))
            if not cursor.fetchone():
                print(f"⚠️ Instructor '{name}' not found.")
                return
            
            cursor.execute("UPDATE instructor SET age = ? WHERE name = ?", (new_age, name))  
            conn.commit()
            print(f"✅ Age updated for '{name}' to {new_age}.")  

        except sqlite3.Error as e:
            print(f"❌ Error updating age: {e}")

    def update_city(self, name, new_city):
        """Updates the instructor's city."""
        try:
            cursor.execute("SELECT name FROM instructor WHERE name = ?", (name,))
            if not cursor.fetchone():
                print(f"⚠️ Instructor '{name}' not found.")
                return
            
            cursor.execute("UPDATE instructor SET city = ? WHERE name = ?", (new_city, name))  
            conn.commit()
            print(f"✅ City updated for '{name}' to '{new_city}'.")  

        except sqlite3.Error as e:
            print(f"❌ Error updating city: {e}")
    
    def add_course(self, course_name, course_code):
        try:
            # Check if the instructor exists
            cursor.execute("SELECT name FROM instructor WHERE name = ?", (self.name,))
            if not cursor.fetchone():
                print(f"⚠️ Instructor '{self.name}' not found. Please add the instructor first.")
                return

            # Check if the course exists in the global 'course_list' table
            cursor.execute("SELECT course_name FROM course_list WHERE course_name = ? AND course_code = ?", 
                        (course_name, course_code))
            if not cursor.fetchone():
                print(f"⚠️ Course '{course_name}' (Code: {course_code}) is not available in the course list.")
                return

            # Insert the course into the instructor's personal course table
            cursor.execute(f"""
                INSERT INTO "{self.name}_courses" (course_name, course_code) 
                VALUES (?, ?)
            """, (course_name, course_code))
            
            conn.commit()
            print(f"✅ Course '{course_name}' (Code: {course_code}) added for '{self.name}'.")

        except sqlite3.IntegrityError:
            print(f"⚠️ Course '{course_name}' already exists for '{self.name}'.")
        except sqlite3.Error as e:
            print(f"❌ Error adding course: {e}")

    def remove_course_from_instructor(self,instructor_name, course_name, course_code):
        try:
            # Check if the instructor exists
            cursor.execute("SELECT name FROM instructor WHERE name = ?", (instructor_name,))
            if not cursor.fetchone():
                print(f"⚠️ Instructor '{instructor_name}' not found.")
                return

            # Check if the course exists in the instructor's course list
            cursor.execute(f"SELECT * FROM \"{instructor_name}_courses\" WHERE course_name = ? AND course_code = ?", 
                        (course_name, course_code))
            if not cursor.fetchone():
                print(f"⚠️ Course '{course_name}' (Code: {course_code}) not found in '{instructor_name}'s course list.")
                return

            # Remove the course from the instructor's personal course table
            cursor.execute(f"DELETE FROM \"{instructor_name}_courses\" WHERE course_name = ? AND course_code = ?", 
                        (course_name, course_code))
            conn.commit()
            print(f"✅ Course '{course_name}' (Code: {course_code}) removed from '{instructor_name}'s course list.")

        except sqlite3.Error as e:
            print(f"❌ Error removing course: {e}")

    def show_enrolled_courses(self):
        try:
            # Check if instructor exists
            cursor.execute("SELECT name FROM instructor WHERE name = ?", (self.name,))
            if not cursor.fetchone():
                print(f"⚠️ Instructor '{self.name}' not found.")
                return
            # Fetch courses from the instructor's personal course table
            cursor.execute(f"SELECT course_name, course_code FROM \"{self.name}_courses\"")
            courses = cursor.fetchall()

            if not courses:
                print(f"⚠️ No courses found for '{self.name}'.")
                return
            # Display courses
            print(f"📚 Courses assigned to '{self.name}':")
            print("Course Name | Course Code")
            print("-" * 30)
            for course_name, course_code in courses:
                print(f"{course_name} | {course_code}")

        except sqlite3.Error as e:
            print(f"❌ Error fetching courses: {e}")

    def check_students_enrolled(self, course_name, course_code):
        try:
            # Get all student tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_courses'")
            student_tables = cursor.fetchall()

            enrolled_students = []

            for (table_name,) in student_tables:
                # Check if 'course_grade' column exists in this student's course table
                cursor.execute(f"PRAGMA table_info(\"{table_name}\")")
                columns = [col[1] for col in cursor.fetchall()]
                
                if "course_grade" not in columns:  
                    # Add 'course_grade' column if missing
                    cursor.execute(f"ALTER TABLE \"{table_name}\" ADD COLUMN course_grade TEXT")
                    conn.commit()

                # Fetch course details along with grade
                cursor.execute(f"""
                    SELECT course_grade FROM \"{table_name}\" 
                    WHERE course_name = ? AND course_code = ?
                """, (course_name, course_code))
                result = cursor.fetchone()

                if result is not None:  # If student is enrolled in the course
                    student_name = table_name.replace("_courses", "")  # Extract student name from table name
                    
                    # Skip if the student is an instructor
                    cursor.execute("SELECT name FROM instructor WHERE name = ?", (student_name,))
                    if cursor.fetchone():
                        continue  

                    course_grade = result[0] if result[0] is not None else "N/A"  # Handle NULL grade
                    enrolled_students.append((student_name, course_grade))

            # Display results
            if enrolled_students:
                print(f"✅ Students enrolled in '{course_name}' (Code: {course_code}):")
                for student, course_grade in enrolled_students:
                    print(f"- {student} | Grade: {course_grade}")
            else:
                print(f"⚠️ No students found enrolled in '{course_name}' (Code: {course_code}').")

        except sqlite3.Error as e:
            print(f"❌ Error checking enrolled students: {e}")

    def assign_grades(self, course_name, course_code):
        try:
            # Get all student tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_courses'")
            student_tables = cursor.fetchall()

            enrolled_students = []

            for (table_name,) in student_tables:
                # Check if student is enrolled in the course
                cursor.execute(f"SELECT * FROM \"{table_name}\" WHERE course_name = ? AND course_code = ?", 
                            (course_name, course_code))
                if cursor.fetchone():  
                    student_name = table_name.replace("_courses", "")  # Extract student name from table name
                    
                    # Skip if the student is an instructor
                    cursor.execute("SELECT name FROM instructor WHERE name = ?", (student_name,))
                    if cursor.fetchone():
                        continue  

                    enrolled_students.append(student_name)

            # If no students are enrolled, return
            if not enrolled_students:
                print(f"⚠️ No students found enrolled in '{course_name}' (Code: {course_code}').")
                return

            # Ensure 'course_grade' column exists in student course tables
            for student in enrolled_students:
                cursor.execute(f"PRAGMA table_info(\"{student}_courses\")")
                columns = [col[1] for col in cursor.fetchall()]
                if "course_grade" not in columns:
                    cursor.execute(f"ALTER TABLE \"{student}_courses\" ADD COLUMN course_grade TEXT")
                    conn.commit()

            # Assign grades to each student
            for student in enrolled_students:
                grade = input(f"Enter grade for {student} in '{course_name}': ").upper()  # Get grade input
                cursor.execute(f"""
                    UPDATE \"{student}_courses\" 
                    SET course_grade = ? 
                    WHERE course_name = ? AND course_code = ?
                """, (grade, course_name, course_code))
                conn.commit()
                print(f"✅ Grade '{grade}' assigned to {student} for '{course_name}'.")

        except sqlite3.Error as e:
            print(f"❌ Error assigning grades: {e}")

    def update_student_grade(self, student_name, course_name, course_code, new_grade):
        try:
            table_name = f"{student_name}_courses"
            
            # Check if the student has the course
            cursor.execute(f"""
                SELECT course_grade FROM "{table_name}" 
                WHERE course_name = ? AND course_code = ?
            """, (course_name, course_code))
            
            if cursor.fetchone() is None:
                print(f"⚠️ No record found for {student_name} in '{course_name}' (Code: {course_code}).")
                return

            # Update the grade
            cursor.execute(f"""
                UPDATE "{table_name}" 
                SET course_grade = ? 
                WHERE course_name = ? AND course_code = ?
            """, (new_grade, course_name, course_code))
            conn.commit()

            print(f"✅ Grade updated to '{new_grade}' for {student_name} in '{course_name}'.")

        except sqlite3.Error as e:
            print(f"❌ Error updating grade: {e}")


    # def check_student_courses(self, student_name):
    #     try:
    #         student_table = f"{student_name}_courses"

    #         # Check if the student's course table exists
    #         cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (student_table,))
    #         if not cursor.fetchone():
    #             print(f"⚠️ Student '{student_name}' does not exist or has no enrolled courses.")
    #             return

    #         # Fetch and display all course records for the student
    #         cursor.execute(f"SELECT * FROM \"{student_table}\"")
    #         courses = cursor.fetchall()

    #         if not courses:
    #             print(f"⚠️ No courses found for '{student_name}'.")
    #             return

    #         # Get column names dynamically
    #         cursor.execute(f"PRAGMA table_info(\"{student_table}\")")
    #         columns = [col[1] for col in cursor.fetchall()]
    #         print(" | ".join(columns))

    #         # Print course data
    #         for row in courses:
    #             print(" | ".join(str(value) for value in row))

    #     except sqlite3.Error as e:
    #         print(f"❌ Error retrieving courses: {e}")
