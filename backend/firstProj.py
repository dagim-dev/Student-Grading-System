import json
import os
from datetime import datetime

FILENAME = "students_data.json"  # Main JSON file where all student data will be saved and loaded from
BACKUP_FOLDER = "backups"        # Folder to store backup copies of the student data file

# Dictionary to store all students and their subjects/grades
# Structure: { "Student Name": { "Subject": [list of grades] } }
students = {}


# Helper functions


def normalize_name(name):
    """Normalize student names to title case."""
    return name.strip().title()

def normalize_subject(subject):
    """Normalize subject names to title case."""
    return subject.strip().title()

def letter_grade(avg):
    """Convert numeric average to letter grade."""
    if avg >= 90:
        return "A+"
    elif avg >= 85:
        return "A"
    elif avg >= 80:
        return "A-"
    elif avg >= 75:
        return "B+"
    elif avg >= 70:
        return "B"
    elif avg >= 65:
        return "C+"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


# Core functions


def addStudent(name):
    name = normalize_name(name)
    if name not in students:
        students[name] = {}
        print(f"Student '{name}' added successfully.")
    else:
        print(f"The student '{name}' is already in the record!")



def setGrade(name, subject, grade):
    name = normalize_name(name)
    subject = normalize_subject(subject)

    # Auto-create student if missing
    if name not in students:
        students[name] = {}

    if not isinstance(grade, list):
        grade = [grade]

    for g in grade:
        if not isinstance(g, (int, float)):
            return {
                "success": False,
                "message": "Grades must be numbers"
            }

    if subject in students[name]:
        students[name][subject].extend(grade)
    else:
        students[name][subject] = grade

    return {
        "success": True,
        "message": f"Grades added for {name} in {subject}"
    }


def removeGrade(name, subject, grade):
    name = normalize_name(name)
    subject = normalize_subject(subject)

    if not isinstance(grade, (int, float)):
        print(f"Invalid grade input: {grade}. Must be a number.")
        return

    if name not in students:
        print("This person is not in the record.")
        return
    if subject not in students[name]:
        print(f"{name} is not taking the subject '{subject}'.")
        return
    if grade in students[name][subject]:
        students[name][subject].remove(grade)
        print(f"Grade {grade} removed from {subject} for {name}.")
        if not students[name][subject]:
            print(f"{name} now has no grades for {subject}.")
    else:
        print(f"The grade {grade} does not exist in {subject} for {name}.")

def displayReport(name):
    name = normalize_name(name)
    if name not in students:
        print("This student is not in our record.")
        return

    print("\n" + "="*50)
    print(f"REPORT FOR {name}")
    print("="*50)
    
    student_data = students[name]
    allGrades = []

    if not student_data:
        print("No subjects or grades available.")
        return

    for subject in sorted(student_data):
        # Filter numeric grades
        grades = [g for g in student_data[subject] if isinstance(g, (int, float))]

        if not grades:
            print(f"{subject:<15}: No grades available")
            continue

        subject_avg = sum(grades)/len(grades)
        allGrades.extend(grades)
        print(f"{subject:<15}: {grades} | Avg: {subject_avg:.2f} | Letter: {letter_grade(subject_avg)}")

    if allGrades:
        overall_avg = sum(allGrades)/len(allGrades)
        print("-"*50)
        print(f"Overall Average: {overall_avg:.2f} | Letter: {letter_grade(overall_avg)}")
    print("="*50 + "\n")




def getStudentReport(name):
    name = normalize_name(name)
    if name not in students:
        return {"success": False, "message": f"Student '{name}' not found."}

    student_data = students[name]
    report = {
        "name": name,
        "subjects": {},
        "overall_average": None,
        "overall_letter": None
    }

    all_grades = []

    for subject, grades_list in student_data.items():
        # Filter numeric grades
        grades = [g for g in grades_list if isinstance(g, (int, float))]
        if not grades:
            continue
        subject_avg = sum(grades) / len(grades)
        all_grades.extend(grades)
        report["subjects"][subject] = {
            "grades": grades,
            "average": subject_avg,
            "letter": letter_grade(subject_avg)
        }

    if all_grades:
        overall_avg = sum(all_grades) / len(all_grades)
        report["overall_average"] = overall_avg
        report["overall_letter"] = letter_grade(overall_avg)

    report["success"] = True
    return report




def removeStudents(names):
    for name in names:
        name = normalize_name(name)
        if name in students:
            students.pop(name)
            print(f"{name} has been removed.")
        else:
            print(f"{name} was not found in the record.")



def displayAllStudent():
    for name in students:
        displayReport(name)



def searchStudent(name):
    name = normalize_name(name)
    if name in students:
        displayReport(name)
    else:
        print(f"Student '{name}' not found in the record.")



def subjectAverage(subject):
    subject = normalize_subject(subject)
    allGrades = []

    for student in students:
        grades = [g for g in students[student].get(subject, []) if isinstance(g, (int, float))]
        allGrades.extend(grades)

    if not allGrades:
        print(f"No grades found for the subject '{subject}'.")
        return

    avg = sum(allGrades)/len(allGrades)
    print(f"The average grade for {subject} is {avg:.2f} | Letter: {letter_grade(avg)}")




def getSubjectAverage(subject):
    subject = normalize_subject(subject)
    all_grades = []

    for student in students:
        grades = [g for g in students[student].get(subject, []) if isinstance(g, (int, float))]
        all_grades.extend(grades)

    if not all_grades:
        return {"success": False, "message": f"No grades found for {subject}"}

    avg = sum(all_grades) / len(all_grades)
    return {"success": True, "subject": subject, "average": round(avg, 2), "letter": letter_grade(avg)}




def rank_students():
    student_averages = {}
    for student, subjects in students.items():
        all_grades = []
        for grades in subjects.values():
            all_grades.extend([g for g in grades if isinstance(g, (int, float))])
        if all_grades:
            student_averages[student] = sum(all_grades)/len(all_grades)

    if not student_averages:
        print("No students with grades to rank.")
        return

    sorted_students = sorted(student_averages.items(), key=lambda x: x[1], reverse=True)

    print("\nSTUDENT RANKINGS")
    print("="*50)
    rank = 1
    prev_avg = None
    for i, (student, avg) in enumerate(sorted_students):
        if prev_avg is not None and avg == prev_avg:
            print(f"{rank}. {student:<20} — {avg:.2f} | {letter_grade(avg)}")
        else:
            rank = i + 1
            print(f"{rank}. {student:<20} — {avg:.2f} | {letter_grade(avg)}")
        prev_avg = avg
    print("="*50 + "\n")





def getRankings():
    student_averages = {}
    for student, subjects in students.items():
        all_grades = []
        for grades in subjects.values():
            all_grades.extend([g for g in grades if isinstance(g, (int, float))])
        if all_grades:
            student_averages[student] = sum(all_grades)/len(all_grades)

    if not student_averages:
        return {"success": False, "message": "No students with grades to rank."}

    # Sort students by average descending
    sorted_students = sorted(student_averages.items(), key=lambda x: x[1], reverse=True)

    rankings = []
    rank = 1
    prev_avg = None

    for i, (student, avg) in enumerate(sorted_students):
        if prev_avg is not None and avg == prev_avg:
            pass  # same rank
        else:
            rank = i + 1
        rankings.append({
            "rank": rank,
            "name": student,
            "average": round(avg, 2),
            "letter": letter_grade(avg)
        })
        prev_avg = avg

    return {"success": True, "rankings": rankings}


# Save & Load


def save_data(students_dict, create_backup=True):
    if create_backup and not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    if create_backup and os.path.exists(FILENAME):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_FOLDER, f"students_backup_{timestamp}.json")
        try:
            with open(FILENAME, "r") as f:
                data = f.read()
            with open(backup_file, "w") as f:
                f.write(data)
            print(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"Warning: Backup could not be created. {e}")
    try:
        with open(FILENAME, "w") as f:
            json.dump(students_dict, f, indent=4)
        print(f"Student data saved successfully to {FILENAME}.")
    except Exception as e:
        print(f"Error saving data: {e}")



def load_data():
    if not os.path.exists(FILENAME):
        print(f"No saved data found. Starting with empty record.")
        return {}
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
        print(f"Student data loaded successfully from {FILENAME}.")
        return data
    except json.JSONDecodeError:
        print("Error: Saved data file is corrupted. Starting with empty record.")
        return {}
    except Exception as e:
        print(f"Error loading data: {e}. Starting with empty record.")
        return {}


# Menu-driven interface
# -------------------------------

def main_menu():
    global students
    students = load_data()

    while True:
        print("\n" + "="*50)
        print("      STUDENT GRADING SYSTEM MENU")
        print("="*50)
        print("1. Add a new student")
        print("2. Add or update grades for a student")
        print("3. Remove a specific grade from a student")
        print("4. Display a student's report")
        print("5. Display all students' reports")
        print("6. Remove student(s)")
        print("7. Search for a student")
        print("8. Calculate class/subject average")
        print("9. Rank students by average")
        print("10. Save data")
        print("11. Exit")
        print("="*50)

        choice = input("Enter your choice (1-11): ").strip()
        if not choice.isdigit() or int(choice) not in range(1, 12):
            print("Invalid choice! Enter a number from 1 to 11.")
            continue
        choice = int(choice)

        if choice == 1:
            name = input("Enter student's name: ").strip()
            if name:
                addStudent(name)
            else:
                print("Name cannot be empty.")
        elif choice == 2:
            name = input("Enter student's name: ").strip()
            subject = input("Enter subject: ").strip()
            grades_input = input("Enter grade(s) separated by commas: ").strip()
            try:
                grades = [float(g.strip()) for g in grades_input.split(",")]
            except ValueError:
                print("Invalid grades! Enter numbers only, separated by commas.")
                continue
            setGrade(name, subject, grades)
        elif choice == 3:
            name = input("Enter student's name: ").strip()
            subject = input("Enter subject: ").strip()
            grade_input = input("Enter grade to remove: ").strip()
            try:
                grade = float(grade_input)
            except ValueError:
                print("Invalid grade! Must be a number.")
                continue
            removeGrade(name, subject, grade)
        elif choice == 4:
            name = input("Enter student's name: ").strip()
            displayReport(name)
        elif choice == 5:
            displayAllStudent()
        elif choice == 6:
            names_input = input("Enter student names to remove (comma-separated): ").strip()
            names_list = [n.strip() for n in names_input.split(",") if n.strip()]
            if names_list:
                removeStudents(names_list)
            else:
                print("No valid names entered.")
        elif choice == 7:
            name = input("Enter student name to search: ").strip()
            searchStudent(name)
        elif choice == 8:
            subject = input("Enter subject to calculate average for: ").strip()
            if subject:
                subjectAverage(subject)
            else:
                print("Subject cannot be empty.")
        elif choice == 9:
            rank_students()
        elif choice == 10:
            save_data(students)
        elif choice == 11:
            print("Saving data before exiting...")
            save_data(students)
            print("Goodbye!")
            break

# Run the program
if __name__ == "__main__":
    main_menu()
