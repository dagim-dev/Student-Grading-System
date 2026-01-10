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

students = {}

def addStudent(name):
    
    if name not in students: 
        
        students[name] = {}

        print ("Student added succesfully.")

        print(students)
    
    else:
        print("The student is already in the record!")



addStudent("Dagi")
addStudent("Kat")




def setGrade(name, subject, grade):

    if name not in students:
        decision = input("The student is not in the record. Do you want to add them as a new student? Yes or no? ")

        if decision.lower() == "no":
            print("Can not add a grade and a subject for a student that is not in the record. Put student in the record first.")
            return

        elif decision.lower() == "yes":
            addStudent(name)

            students[name][subject] = [grade]

            print(students)
        
        else:
            print("Invalid input. Please type only yes or no.")
            return
        
    else:

        students[name][subject] = [grade]

        print(students)    

setGrade("Kat", "math", (91,99,23))


def removeGrade(name, subject, grade):

    if name not in students:
        print("This person is not in the record.")

    if subject not in students[name]:
        print(name + " is not taking this subject.")

    if students[name][subject] == [grade]:

        students[name][subject].remove(grade)



    else:
        print("The grade doesn't match.")






