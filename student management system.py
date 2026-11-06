import json
import os


class Student:
    def __init__(self, student_id, name, age, department, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.marks = marks

    def display(self):
        print("\n---------- STUDENT DETAILS ----------")
        print(f"Student ID : {self.student_id}")
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Department : {self.department}")
        print(f"Marks      : {self.marks}")
        print("-------------------------------------")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "marks": self.marks
        }


class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.filename = "students.json"
        self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)

                for item in data:
                    student = Student(
                        item["student_id"],
                        item["name"],
                        item["age"],
                        item["department"],
                        item["marks"]
                    )
                    self.students[student.student_id] = student

            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                print("Warning: Could not load student records.")

    def save_students(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [student.to_dict() for student in self.students.values()],
                file,
                indent=4
            )

    def add_student(self):
        student_id = input("Enter Student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty!")
            return

        if student_id in self.students:
            print("Student ID already exists!")
            return

        name = input("Enter Student Name: ").strip()

        if not name:
            print("Name cannot be empty!")
            return

        try:
            age = int(input("Enter Age: "))

            if age <= 0:
                print("Age must be greater than zero!")
                return

            department = input("Enter Department: ").strip()

            if not department:
                print("Department cannot be empty!")
                return

            marks = float(input("Enter Marks (0-100): "))

            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100!")
                return

        except ValueError:
            print("Please enter valid numbers for age and marks!")
            return

        student = Student(student_id, name, age, department, marks)
        self.students[student_id] = student

        try:
            self.save_students()
            print("\nStudent added successfully!")
        except OSError:
            del self.students[student_id]
            print("Error: Could not save student records.")

    def view_students(self):
        if not self.students:
            print("\nNo student records found!")
            return

        print("\n========== ALL STUDENTS ==========")

        for student in self.students.values():
            student.display()

    def search_student(self):
        student_id = input("Enter Student ID to search: ").strip()

        student = self.students.get(student_id)

        if student:
            student.display()
        else:
            print("Student not found!")

    def update_student(self):
        student_id = input("Enter Student ID to update: ").strip()
        student = self.students.get(student_id)

        if student is None:
            print("Student not found!")
            return

        print("\nPress Enter to keep the existing value.")

        name = input(f"Name [{student.name}]: ").strip()
        age_input = input(f"Age [{student.age}]: ").strip()
        department = input(
            f"Department [{student.department}]: "
        ).strip()
        marks_input = input(f"Marks [{student.marks}]: ").strip()

        try:
            age = student.age if not age_input else int(age_input)
            marks = student.marks if not marks_input else float(marks_input)

            if age <= 0:
                print("Age must be greater than zero!")
                return

            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100!")
                return

        except ValueError:
            print("Invalid age or marks!")
            return

        old_values = (
            student.name,
            student.age,
            student.department,
            student.marks
        )

        if name:
            student.name = name

        student.age = age

        if department:
            student.department = department

        student.marks = marks

        try:
            self.save_students()
            print("Student updated successfully!")

        except OSError:
            (
                student.name,
                student.age,
                student.department,
                student.marks
            ) = old_values

            print("Error: Could not save updated records.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ").strip()

        if student_id not in self.students:
            print("Student not found!")
            return

        confirm = input("Are you sure you want to delete? (yes/no): ")
        
        if confirm.strip().lower() != "yes":
            print("Deletion cancelled.")
            return

        student = self.students.pop(student_id)

        try:
            self.save_students()
            print("Student deleted successfully!")

        except OSError:
            self.students[student_id] = student
            print("Error: Could not save changes.")

    def menu(self):
        while True:
            print("\n========================================")
            print("      STUDENT MANAGEMENT SYSTEM")
            print("========================================")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")
            print("========================================")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                print("\nThank you for using Student Management System!")
                break

            else:
                print("\nInvalid choice! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    system = StudentManagementSystem()
    system.menu()
