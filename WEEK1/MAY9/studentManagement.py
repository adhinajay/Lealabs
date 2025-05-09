class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}"

class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student_id, name, age):
        student = Student(student_id, name, age)
        self.students.append(student)
        print("Student",name,"added successfully.")

    def remove_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print("Student with ID",student_id,"removed.")
                return
        print("Student not found.")

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                print("Student found:")
                print(student)
                return
        print("Student not found.")

    def display_all(self):
        if not self.students:
            print("No students in the system.")
        else:
            print("All Students:")
            for student in self.students:
                print(student)

def main():
    manager = StudentManager()
    
    #Input command from user
    while True:
        print("\nStudent Management System")
        print(" 1.Add Student")
        print(" 2.Remove Student")
        print(" 3.Search Student")
        print(" 4.Display All Students")
        print(" 5.Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            student_id = int(input("Enter student ID: "))
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            manager.add_student(student_id, name, age)
        elif choice == "2":
            student_id = int(input("Enter student ID to remove: "))
            manager.remove_student(student_id)
        elif choice == "3":
            student_id = int(input("Enter student ID to search: "))
            manager.search_student(student_id)
        elif choice == "4":
            manager.display_all()
        elif choice == "5":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
