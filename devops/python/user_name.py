student_grades = {
    "One": "A",
    "Two": "B",
    "Three": "C",
}

print("Choose an option:")
print("1. Add a new student")
print("2. Update an existing student grade")
print("3. Print all student grades")

choice = input("Enter your choice (1/2/3): ")

if choice == "1":
    name = input("Enter student name: ")
    grade = input("Enter grade: ")
    student_grades[name] = grade
    print(f"Added {name} with grade {grade}.")
elif choice == "2":
    name = input("Enter student name to update: ")
    if name in student_grades:
        grade = input("Enter new grade: ")
        student_grades[name] = grade
        print(f"Updated {name} to grade {grade}.")
    else:
        print("Student not found.")
elif choice == "3":
    if student_grades:
        print("Student Grades:")
        for name, grade in student_grades.items():
            print(f"{name}: {grade}")
    else:
        print("No student grades available.")
else:
    print("Invalid choice.")
