"""
This module implements a student grade analyzer application.
"""
from typing import Dict, List, Optional

# Global list of students. Each student is a dictionary with keys:
# "name" (str) and "grades" (list of integers)
students: List[Dict[str, List[int]]] = []

# Menu options
FIRST_OPTION = "Add a new student"
SECOND_OPTION = "Add a grades for a student"
THIRD_OPTION = "Show report (all students)"
FOURTH_OPTION = "Find top performer"
FIFTH_OPTION = "Exit"


def find_student(name: str) -> Optional[Dict[str, List[int]]]:
    """
    Search for a student by name in the global students list.
    :param name: The name of the student to find.
    :return: The student dictionary if found or None if is not found.
    """

    for student in students:
        if student.get("name") == name:
            return student
    return None


def check_input() -> Optional[str]:
    """
    Get and validate user input for a student's name.
    :return: Capitalized and cleaned name string if valid, otherwise None.
    """

    name = ' '.join(input("Enter student name: ").split()).title()
    if not name or not all(
            ind.isalpha() or ind.isspace() or ind == '-' or ind == "'" for ind in name):
        print("Enter valid student name! ")
        return None
    return name


def add_student() -> None:
    """
    Prompt the user to add a new student to the global student list.
    The function:
    1. Remove extra spaces from input and normalize capitalization.
    2. Check for empty input and prompt again if necessary.
    3. Check if a student with the same name already exists.
    4. Add the student with an empty list of grades if valid.
    """

    while True:
        name = check_input()
        if name is None:
            continue
        if find_student(name):
            print(f"The name {name} already exists.")
            continue

        students.append({"name": name, "grades": []})
        break  # Student successfully added — exit the loop


def valid_input(input_grade: str) -> int | str | None:
    """
    Check if input is a valid grade (0-100) or 'done'.
    :param input_grade: string from user input
    :return: int (0-100) if valid, "done" if finished, or None if invalid
    """

    if input_grade.lower() == "done":
        return "done"
    try:
        value = int(input_grade)
        if 0 <= value <= 100:
            return value
        return None
    except ValueError:
        return None


def add_grades() -> None:
    """
    Add grades to an existing student.
    - Asks for the student's name.
    - Checks if student exists.
    - Loops to input grades until 'done' is entered.
    - Validates grades (0-100).
    """

    while True:
        name = check_input()
        if name is None:
            continue
        student = find_student(name)
        if not student:
            print(f"The student '{name}' is not found.")
            return  # exit function to go back to menu

        while True:
            grade = input("Enter a grade(or 'done' to finish): ")
            result = valid_input(grade)
            if result == "done":
                break
            if result is not None:
                student["grades"].append(result)
            else:
                print("Invalid input. Please enter a number (or 'done'): ")
        break


def show_report() -> None:
    """
    Display all students and their average grades.
    Also show max, min, and overall averages.
    """

    if not students:
        print("No students available.")
        return
    print("-----Student Report-----")
    # Collect all students' average grades for the final summary
    averages: List[float] = []
    for student in students:
        name = student["name"]
        grades = student["grades"]
        try:
            average_grade = round((sum(grades) / len(grades)), 1)
            print(f"{name}'s average grade is {average_grade}.")
            averages.append(average_grade)

        except ZeroDivisionError:
            print(f"{name}'s average grade is N/A.")

    if averages:
        max_average = round(max(averages), 1)
        min_average = round(min(averages), 1)
        overall_average = round(sum(averages) / len(averages), 1)

        print("-------------------------")
        print(f"Max average: {max_average}")
        print(f"Min average: {min_average}")
        print(f"Overall average: {overall_average}")
    else:
        print("No grades available for summary.")


def find_top_performer() -> None:
    """
    Find and display the student with the highest average grade.
    Handles cases where there are no students or no grades.
    """

    if not students:
        print("No students available.")
        return

    students_with_grades = [student for student in students if student["grades"]]
    if not students_with_grades:
        print("No grades available")
        return
    top_student = max(
        students_with_grades,
        key=lambda student: sum(
            student["grades"]) / len(student["grades"])
    )

    average_grade = round(
        (sum(top_student["grades"]) / len(top_student["grades"])), 1)
    print(
        f"The student with the highest average is {top_student['name']} "
        f"with a grade of {average_grade}"
    )


def exit_5() -> None:
    """Print exit message."""

    print("Exiting program")


def menu(select: int) -> None:
    """
    Execute the function corresponding to the user's menu choice.
    :param select: Menu option number (1-5)
    """

    if select == 1:
        add_student()
    elif select == 2:
        add_grades()
    elif select == 3:
        show_report()
    elif select == 4:
        find_top_performer()
    elif select == 5:
        exit_5()


options = [FIRST_OPTION, SECOND_OPTION, THIRD_OPTION, FOURTH_OPTION, FIFTH_OPTION]

# Main program loop
while True:
    print("-----Student Grade Analyzer------")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Enter number from 1 to 5: ")
        continue
    if choice > 5 or choice < 1:
        print("Enter number from 1 to 5: ")
        continue
    menu(choice)
    if choice == 5:
        break
