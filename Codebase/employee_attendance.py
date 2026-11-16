import os
import json
from datetime import datetime

FILENAME = "attendance.txt"


# 1. Load data from file
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            content = file.read().strip()

            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return []

    return []


# 2. Save data to file
def save_data(employees):
    with open(FILENAME, "w") as file:
        json.dump(employees, file, indent=4)


# 3. Add Employee
def add_employee(employees):

    employee_id = f"E{101 + len(employees)}"

    name = input("Enter employee name: ").strip()

    if not name:
        print("Error: Name cannot be empty.")
        return

    new_employee = {
        "id": employee_id,
        "name": name,
        "attendance": {}
    }

    employees.append(new_employee)
    save_data(employees)

    print(f"Employee added: {employee_id} | {name}")


# 4. Mark Attendance
def mark_attendance(employees):

    emp_id = input("Enter Employee ID: ").strip()

    emp = None

    for e in employees:
        if e["id"] == emp_id:
            emp = e
            break

    if not emp:
        print(f"Employee {emp_id} not found.")
        return

    date = input("Enter date (YYYY-MM-DD): ").strip()

    # Validate exact date format
    try:
        valid_date = datetime.strptime(date, "%Y-%m-%d")

        if valid_date.strftime("%Y-%m-%d") != date:
            raise ValueError

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    # Check duplicate attendance
    if date in emp["attendance"]:
        print(f"Attendance for {date} is already marked.")
        return

    # Validate status
    status = input(
        "Enter status (P for Present, A for Absent, L for Leave): "
    ).strip().upper()

    if status not in ["P", "A", "L"]:
        print("Invalid status. Enter P, A or L.")
        return

    emp["attendance"][date] = status

    save_data(employees)

    print(f"Attendance marked successfully for {emp['name']}!")


# 5. View Attendance Report
def view_report(employees):

    emp_id = input("Enter Employee ID to view report: ").strip()

    emp = None

    for e in employees:
        if e["id"] == emp_id:
            emp = e
            break

    if not emp:
        print(f"Employee {emp_id} not found.")
        return

    print(f"\n--- Attendance Report for {emp['name']} ---")

    records = emp["attendance"]

    # Check attendance records
    if not records:
        print(f"{emp['name']}: Present 0 | Absent 0 | Leave 0")
        print("Attendance: 0.00% (no records)")
        return

    present_count = 0
    absent_count = 0
    leave_count = 0

    for date, status in records.items():

        if status == "P":
            present_count += 1

        elif status == "A":
            absent_count += 1

        elif status == "L":
            leave_count += 1

    total_marked = present_count + absent_count + leave_count

    percentage = (present_count / total_marked) * 100

    print(
        f"{emp['name']}: Present {present_count} | "
        f"Absent {absent_count} | Leave {leave_count}"
    )

    print(f"Attendance: {percentage:.2f}%")


# 6. Main Menu
def main():

    employees = load_data()

    while True:

        print("\n===== EMPLOYEE ATTENDANCE SYSTEM =====")
        print("1. Add Employee")
        print("2. Mark Attendance")
        print("3. View Attendance Report")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_employee(employees)

        elif choice == "2":
            mark_attendance(employees)

        elif choice == "3":
            view_report(employees)

        elif choice == "4":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
