""" 
1. Add a student

Input: student name

Action: create a new record for the student

2. Add grades for a student

Input: student name, subject, grade

Action: store the grade under the student’s record

3. Update a grade

Input: student name, subject, new grade

Action: overwrite existing grade

4. Remove a grade

Input: student name, subject

Action: delete that subject from the student’s record

5. Display a student’s report

Show all subjects and grades

Show average grade

6. Calculate average grade for a student

Average of all subjects

7. Remove a student

Input: student name

Action: delete the student from the system

8. Display all students

Show names of all students currently in the system

9. Search for a student

Input: student name

Action: show student record if found

10. Letter grade calculation

Convert numeric average to a letter (A, B, C, etc.)

11. Menu-driven interface

Let the user choose actions via numbered menu

12. Class/Subject average

Calculate average grade for a subject across all students

13. Rank students

Show students ranked by average grade

14. Save and load data

Save all student data to a file (JSON or CSV)

Load data from file on program start

15. Error handling

Handle invalid input (e.g., letters instead of numbers for grades)

Handle missing students/subjects

16. User-friendly display

Format reports neatly with alignment, headers, etc.

17. Optional GUI

Later, you could use Tkinter for a simple graphical interface


18. Exit program

Cleanly end the program
"""

# Dictionary to store all students and their subjects/grades
# Structure: { "Student Name": { "Subject": [list of grades] } }

students = {}

# A function to add new students
def addStudent(name):
    
    if name not in students: 
        
        students[name] = {}

        print ("Student added succesfully.")
    
    else:
        print("The student is already in the record!")





def setGrade(name, subject, grade):

    if name not in students:
        decision = input("The student is not in the record. Do you want to add them as a new student? Yes or no? ")

        if decision.lower() == "no":
            print("Can not add a grade and a subject for a student that is not in the record. Put student in the record first.")
            return

        elif decision.lower() == "yes":
            addStudent(name)
        
        else:
            print("Invalid input. Please type only yes or no.")
            return
        

    if not isinstance(grade, list):
        grade = [grade]

    if subject in students[name]:
        students[name][subject].extend(grade)
        
    else:
        students[name][subject] = grade
        
        
setGrade("Kat", "Math", [91, 99, 23])
setGrade("Kat", "Science", [10, 10, 0])
setGrade("Kat", "Computing", [91, 99, 23])
setGrade("Dagim", "computing", [91, 99, 24])
setGrade("Dagim", "Math", [83, 79, 90])
setGrade("Emu", "Computing", [10, 10, 0])
setGrade("Emu", "Math", [10, 10, 0])
setGrade("Emu", "Science", [10, 10, 0])

print(students)


def removeGrade(name, subject, grade):

    if name not in students:
        print("This person is not in the record.")
        return

    if subject not in students[name]:
        print(name + " is not taking this subject.")
        return

    if grade in students[name][subject]:
        students[name][subject].remove(grade)
        print(f"Grade {grade} removed from {subject} for {name}.")

        # Optional: notify if no grades left in subject
        if not students[name][subject]:
            print(f"{name} now has no grades for {subject}.")

    else:
        print(f"The grade {grade} does not exist in {subject} for {name}.")





# Displays student's report
def displayReport(name):

    if name not in students:
        print("This student is not in our record.")
        return
    
    print()
    print()
    print("Report for " + name)
    print("*" * 30)
        
    student_data = students[name]
    allGrades = []

    for subject in sorted(student_data):
        grades = student_data[subject]

        if len(grades) == 0:
            print("No grades available")
            continue

        subject_average = sum(grades) / len(grades)
        allGrades.extend(grades)

        print(f"{subject}: {grades} | Average: {subject_average:.2f}")

    if allGrades:
        overall_average = sum(allGrades) / len(allGrades)
        print("*" * 30)
        print("Overall Average:", round(overall_average, 2))
        print()
        print()


    else:
        print("No grades available.")
        





def removeStudents(studentsNames):

    for i in studentsNames:
        if i in students:
            students.pop(i)
            print(i + " has been removed.")   

        else:
            print(i + " was not found")




def displayAllStudent():

    for i in students:
        displayReport(i)




def searchStudent(name):
    if name in students:
        displayReport(name)
    
    else:
        print("Student not found/not in the record.")


# searchStudent("Emu")


def subjectAverage(subject):

    allGrades = []
    averageGrade = 0

    for i in students:
        if subject in students[i]:
            allGrades.extend(students[i][subject])

    if len(allGrades) > 0:   
        averageGrade = sum(allGrades) / len(allGrades)

    else:
        print("There is no one in the record that is taking that class.")
        return


    print("The average grade for " + subject + " is ", averageGrade)

subjectAverage("Math")


def rank_students():
    # Dictionary to store each student's overall average
    student_averages = {}

    for student, subjects in students.items():
        all_grades = []
        
        for grades in subjects.values():
            all_grades.extend(grades)
        
        if all_grades:  # Only calculate if the student has grades
            overall_avg = sum(all_grades) / len(all_grades)
            student_averages[student] = overall_avg
        else:
            # Optionally, include students with no grades with average 0 or skip
            # student_averages[student] = 0
            continue  # Skip students with no grades

    if not student_averages:
        print("No students with grades to rank.")
        return

    # Sort students by average, descending
    sorted_students = sorted(student_averages.items(), key=lambda x: x[1], reverse=True)

    print("\nStudent Rankings:")
    print("*" * 40)

    rank = 1
    prev_avg = None
    for i, (student, avg) in enumerate(sorted_students):
        # Handle ties: same average gets same rank
        if prev_avg is not None and avg == prev_avg:
            print(f"{rank}. {student} — {avg:.2f}")
        else:
            rank = i + 1
            print(f"{rank}. {student} — {avg:.2f}")
        prev_avg = avg

    print("*" * 40)
    print()

rank_students()





    







