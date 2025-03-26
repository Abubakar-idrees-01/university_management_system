from person import Person  
import sqlite3  

# Database Connection
conn = sqlite3.connect("university_database.db")  
cursor = conn.cursor()


class Student(Person):  
    def __init__(self, name, age, city):  
        super().__init__(name, age, city)  
        self.create_student_table()

    def create_student_table(self):
        cursor.execute("""  
            CREATE TABLE IF NOT EXISTS student(  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                name TEXT NOT NULL,  
                age INTEGER NOT NULL,  
                city TEXT NOT NULL  
            )  
        """)  
        conn.commit()

    def add_student(self):
        try:
            cursor.execute("INSERT INTO student (name, age, city) VALUES (?, ?, ?)",  
                           (self.name, self.age, self.city))  
            conn.commit()
            print(f"✅ {self.name} ADDED as a student.")  

            # Create personal courses table for student
            cursor.execute(f"""  
                CREATE TABLE IF NOT EXISTS "{self.name}_courses"(  
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    course_name TEXT UNIQUE,  
                    course_code TEXT NOT NULL,  
                    course_grade TEXT  
                )  
            """)  
            conn.commit()

        except sqlite3.IntegrityError:  
            print(f"⚠️ {self.name} already exists in the database.")  

    def remove_student(self, name):
        try:
            # Delete student's course table
            cursor.execute(f'DROP TABLE IF EXISTS "{name}_courses"')

            # Delete student from the main student table
            cursor.execute("DELETE FROM student WHERE name = ?", (name,))
            
            conn.commit()
            print(f"✅ Student '{name}' and their courses have been removed.")

        except sqlite3.Error as e:
            print(f"❌ Error: {e}")

    def list_of_students(self):  
        cursor.execute("SELECT * FROM student")  
        rows = cursor.fetchall()  

        if not rows:  
            print("⚠️ No students found in the database.")  
            return  

        # Get column names dynamically  
        cursor.execute("PRAGMA table_info(student)")  
        columns = [col[1] for col in cursor.fetchall()]  
        print(" | ".join(columns))  

        # Print student data  
        for row in rows:  
            print(" | ".join(str(value) for value in row))  
    
    def update_name(self, old_name, new_name):
        """Updates the student's name and renames their courses table."""
        try:
            cursor.execute("SELECT name FROM student WHERE name = ?", (old_name,))
            if not cursor.fetchone():
                print(f"⚠️ Student '{old_name}' not found.")
                return
            
            cursor.execute("UPDATE student SET name = ? WHERE name = ?", (new_name, old_name))  
            cursor.execute(f'ALTER TABLE "{old_name}_courses" RENAME TO "{new_name}_courses"')  
            conn.commit()
            print(f"✅ Student name updated from '{old_name}' to '{new_name}'.")  

        except sqlite3.Error as e:
            print(f"❌ Error updating name: {e}")

    def update_age(self, name, new_age):
        """Updates the student's age."""
        try:
            cursor.execute("SELECT name FROM student WHERE name = ?", (name,))
            if not cursor.fetchone():
                print(f"⚠️ Student '{name}' not found.")
                return
            
            cursor.execute("UPDATE student SET age = ? WHERE name = ?", (new_age, name))  
            conn.commit()
            print(f"✅ Age updated for '{name}' to {new_age}.")  

        except sqlite3.Error as e:
            print(f"❌ Error updating age: {e}")

    def update_city(self, name, new_city):
        """Updates the student's city."""
        try:
            cursor.execute("SELECT name FROM student WHERE name = ?", (name,))
            if not cursor.fetchone():
                print(f"⚠️ Student '{name}' not found.")
                return
            
            cursor.execute("UPDATE student SET city = ? WHERE name = ?", (new_city, name))  
            conn.commit()
            print(f"✅ City updated for '{name}' to '{new_city}'.")  

        except sqlite3.Error as e:
            print(f"❌ Error updating city: {e}")
    
    def add_course(self, course_name, course_code, course_grade=None):  
        try:  
            cursor.execute(f"""  
                INSERT INTO "{self.name}_courses" (course_name, course_code, course_grade)  
                VALUES (?, ?, ?)  
            """, (course_name, course_code, course_grade))  
            conn.commit()  
            print(f"✅ Course '{course_name}' added for {self.name}.")  

        except sqlite3.IntegrityError:  
            print(f"⚠️ Course '{course_name}' already exists for {self.name}.")
    
    def enrolled_course(self):
        name=self.name
        try:
            cursor.execute(f"SELECT * FROM '{name}_courses'")
            rows = cursor.fetchall()

            if not rows:
                print(f"⚠️ No courses found for {name}.")
                return

            # Get column names dynamically  
            cursor.execute(f"PRAGMA table_info('{name}_courses')")
            columns = [col[1] for col in cursor.fetchall()]
            print(" | ".join(columns))  

            # Print all enrolled courses
            for row in rows:
                print(" | ".join(str(value) for value in row))  

        except sqlite3.OperationalError:
            print(f"⚠️ No enrollment records found for {name}.")  
    
    def calculate_student_cgpa(self, student_name):
        try:
            table_name = f"{student_name}_courses"

            # Check if student table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                print(f"⚠️ Student '{student_name}' not found.")
                return

            # Fetch all enrolled courses and grades
            cursor.execute(f"SELECT course_name, course_grade FROM \"{table_name}\" WHERE course_grade IS NOT NULL")
            courses = cursor.fetchall()

            if not courses:
                print(f"⚠️ No valid grades found for '{student_name}'. Cannot calculate CGPA.")
                return

            # Grade to GPA mapping
            grade_points = {"A": 4.0, "B": 3.5, "C": 3.0, "D": 2.5, "E": 2.0, "F": 0.0}

            total_points = 0
            total_courses = 0

            print(f"📜 Courses and Grades for {student_name}:")
            for course, grade in courses:
                grade = grade.strip().upper()  # Normalize grade format
                if grade in grade_points:
                    total_points += grade_points[grade]
                    total_courses += 1
                    print(f"- {course} | Grade: {grade} | Points: {grade_points[grade]}")
                else:
                    print(f"⚠️ Invalid grade '{grade}' in {course}, skipping...")

            if total_courses == 0:
                print(f"⚠️ No valid graded courses found for '{student_name}'.")
                return

            # Calculate CGPA
            cgpa = total_points / total_courses
            print(f"\n🎓 CGPA for {student_name}: {cgpa:.2f}")

        except sqlite3.Error as e:
            print(f"❌ Error calculating CGPA: {e}")

   
    def delete_course(self, course_name):
    
        try:
            cursor.execute(f"DELETE FROM {self.name}_courses WHERE course_name = ?", (course_name,))
            if cursor.rowcount > 0:
                conn.commit()
                print(f"✅ Course '{course_name}' deleted successfully!")
            else:
                print(f"⚠️ Course '{course_name}' not found!")
        except sqlite3.Error as e:
            print(f"❌ Error: {e}")