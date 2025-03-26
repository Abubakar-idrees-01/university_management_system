import sqlite3  
conn = sqlite3.connect("university_database.db")  
cursor = conn.cursor()

class Course:
    def __init__(self,course_name,course_code):  
        self.course_name=course_name
        self.course_code=course_code
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_list(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT  UNIQUE,
            course_code TEXT NOT NULL
        )
    """)
    def add_course_in_list(self):
        try:
            cursor.execute("INSERT INTO course_list (course_name, course_code) VALUES (?, ?)", 
                        (self.course_name, self.course_code))
            conn.commit()
            print(f"Course '{self.course_name}' added successfully!")
        except sqlite3.IntegrityError:
            print(f"Error: Course '{self.course_name}' already exists!")
        
    def show_courses(self):
        cursor.execute("SELECT * FROM course_list")
        rows = cursor.fetchall()
        # Print table headers (column names)
        cursor.execute("PRAGMA table_info(course_list)")  # Get column names
        columns = [col[1] for col in cursor.fetchall()]  # Extract column names
        print(" | ".join(columns))  # Print header row

        # Print all rows in the table
        for row in rows:
            print(" | ".join(str(value) for value in row))  # Print each row
    
    def delete_course(self, course_name):
        cursor.execute("DELETE FROM course_list WHERE course_name = ?", (course_name,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Course '{course_name}' deleted successfully!")
        else:
            print(f"Error: Course '{course_name}' not found!")