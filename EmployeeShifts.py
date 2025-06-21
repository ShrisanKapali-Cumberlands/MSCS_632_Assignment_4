# An application that manages employee shifts in a company.
# Shrisan Kapali
# Student ID: 005032249
# Assignment 4 : Implementing Control Structures

import random
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# GLobal constants for the application
# Days of the week and shifts
DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

SHIFTS = ["Morning", "Afternoon", "Evening"]


# A method that creates a weekly schedule based on employee preferences.
def create_schedule(
    employee_preferences, num_employees_per_shift=2, max_work_days_per_week=5
):

    # Initialize the weekly schedule structure
    weekly_schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS_OF_WEEK}

    # Initialize a counter for days worked by each employee
    employee_work_days = defaultdict(int)
    for emp_name in employee_preferences:
        employee_work_days[emp_name] = 0

    unassigned_employees = []  # To track employees who couldn't be fully scheduled

    print("**********************************************************")
    print("************* Starting Schedule Generation ***************")
    print("**********************************************************")

    # Assigning employees based on their day preferences ---
    # Looping through each day of the week
    for day in DAYS_OF_WEEK:
        print(f"\nCurrently scheduling for {day}:")
        # Need to make sure that each day has at least 2 employees per shift
        # A tracker that helps identify if any employees were assigned for this day
        employees_assigned_today = defaultdict(bool)

        # Bonus implementation: Assigned employees based on their preferences
        # Looping through each employee's preferences
        for employee_name, preferences in employee_preferences.items():
            # As each employee cannot work more than 5 days per week
            if employee_work_days[employee_name] >= max_work_days_per_week:
                print(
                    f"  {employee_name} has reached max work days ({max_work_days_per_week})."
                )
                continue

            # As employee can only work 1 shift per day, we check if they are already assigned today
            # If they are already assigned for this day, skip to the next employee
            if employees_assigned_today[employee_name]:
                continue

            # Get the preferred shifts for the current day from employee preferences
            preferred_shifts_on_day = preferences.get(day, [])

            # If the employee has no preferences for this day, they are unassigned
            assigned_this_day = False
            for preferred_shift in preferred_shifts_on_day:
                # Validate shift name
                if preferred_shift not in SHIFTS:
                    print(
                        f"    Warning: {employee_name} does not prefer working on Shift '{preferred_shift}' for  {day}. Skipping to next."
                    )
                    continue

                # Only if the preferred shift is not full, assign the employee
                if (
                    len(weekly_schedule[day][preferred_shift])
                    < num_employees_per_shift + 1
                ):
                    weekly_schedule[day][preferred_shift].append(employee_name)
                    employees_assigned_today[employee_name] = True
                    employee_work_days[employee_name] += 1
                    print(
                        f"    Assigned {employee_name} to preferred {preferred_shift} on {day}."
                    )
                    assigned_this_day = True
                    break  # Employee assigned for this day, move to next employee
                else:
                    # Preferred shift is full, try next preference if available
                    print(
                        f"    {employee_name}'s preferred {preferred_shift} on {day} is full. Trying next preference."
                    )
                    pass  # Try next preference in the list

            if not assigned_this_day and not employees_assigned_today[employee_name]:
                # If employee couldn't be assigned based on preferences for this day,
                # they are still available for random assignment
                print(
                    f"    {employee_name} could not be assigned based on preferences for {day}."
                )
                pass  # Will be handled in the lower for loop code if needed

        # --- Fill remaining shifts to meet minimums (2 employees per shift) ---
        # And also catch employees who couldn't be assigned by preference but are available
        for shift_type in SHIFTS:
            while len(weekly_schedule[day][shift_type]) < num_employees_per_shift:
                # Find available employees who haven't worked max days and are not assigned today
                available_for_random_assignment = []
                for emp_name in employee_preferences.keys():
                    if (
                        employee_work_days[emp_name] < max_work_days_per_week
                        and not employees_assigned_today[emp_name]
                    ):
                        available_for_random_assignment.append(emp_name)

                if available_for_random_assignment:
                    # Randomly pick an employee from the available pool
                    chosen_employee = random.choice(available_for_random_assignment)
                    weekly_schedule[day][shift_type].append(chosen_employee)
                    employees_assigned_today[chosen_employee] = True
                    employee_work_days[chosen_employee] += 1
                    print(
                        f"    Randomly assigned {chosen_employee} to {shift_type} on {day} to meet minimum."
                    )
                else:
                    print(
                        f"    WARNING: Could not meet minimum of {num_employees_per_shift} for {shift_type} on {day}. Current: {len(weekly_schedule[day][shift_type])}"
                    )
                    break  # Cannot find more employees for this shift

    # For not working Employees
    for emp_name, days_worked in employee_work_days.items():
        if days_worked == 0:
            unassigned_employees.append(emp_name)

    print("\n--- Schedule Generation Complete ---")

    return weekly_schedule, employee_work_days, unassigned_employees


# A method to print the generated schedule in a readable format.
def display_schedule(schedule, employee_work_days):
    print("\n" + "=" * 50)
    print("                 FINAL WEEKLY SCHEDULE")
    print("=" * 50)

    for day in DAYS_OF_WEEK:
        print(f"\n--- {day.upper()} ---")
        for shift_type in SHIFTS:
            employees = schedule[day][shift_type]
            if employees:
                print(f"  {shift_type:<10}: {', '.join(employees)}")
            else:
                print(f"  {shift_type:<10}: No employees assigned")

    print("\n" + "=" * 50)
    print("                 EMPLOYEE WORK DAYS SUMMARY")
    print("=" * 50)
    for employee, days in sorted(employee_work_days.items()):
        print(f"{employee:<15}: {days} days worked")
    print("=" * 50)


# Showing the schedule in a colorful calendar-style Tkinter GUI
def display_schedule_ui(schedule):
    SHIFT_COLORS = {
        "Morning": "#ffffff",
        "Afternoon": "#ffffff",
        "Evening": "#ffffff",
    }

    HEADER_BG = "#2196f3"  # Dark blue-gray
    HEADER_FG = "white"
    SHIFT_HEADER_BG = "#2196f3"
    SHIFT_HEADER_FG = "white"

    root = tk.Tk()
    root.title("Weekly Employee Schedule")

    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10), padding=5)

    # Create main frame
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=0, sticky="NSEW")

    # Column headers: Days
    for col, day in enumerate([""] + DAYS_OF_WEEK):
        bg = HEADER_BG if col != 0 else SHIFT_HEADER_BG
        fg = HEADER_FG if col != 0 else SHIFT_HEADER_FG
        header = tk.Label(
            main_frame,
            text=day,
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg=fg,
            padx=10,
            pady=5,
            relief="ridge",
            bd=2,
        )
        header.grid(row=0, column=col, sticky="NSEW")

    # Shift rows and schedule cells
    for row, shift in enumerate(SHIFTS, start=1):
        # Shift label (left column)
        tk.Label(
            main_frame,
            text=shift,
            font=("Segoe UI", 10, "bold"),
            bg=SHIFT_HEADER_BG,
            fg=SHIFT_HEADER_FG,
            padx=10,
            pady=5,
            relief="ridge",
            bd=2,
        ).grid(row=row, column=0, sticky="NSEW")

        for col, day in enumerate(DAYS_OF_WEEK, start=1):
            employees = schedule[day][shift]
            bg_color = SHIFT_COLORS.get(shift, "#ffffff")
            cell_text = "\n".join(employees) if employees else "No one assigned"
            fg_color = "#000000" if employees else "#888888"

            # Create schedule cell
            tk.Label(
                main_frame,
                text=cell_text,
                bg=bg_color,
                fg=fg_color,
                font=("Segoe UI", 9),
                padx=5,
                pady=5,
                justify="center",
                relief="solid",
                bd=1,
                wraplength=120,
            ).grid(row=row, column=col, sticky="NSEW")

    # Grid expand/resizing
    for i in range(len(DAYS_OF_WEEK) + 1):
        main_frame.columnconfigure(i, weight=1)
    for i in range(len(SHIFTS) + 1):
        main_frame.rowconfigure(i, weight=1)

    root.mainloop()


# Display a summary of employee work days in a separate UI window
def display_employee_summary_ui(employee_work_days):
    root = tk.Tk()
    root.title("Employee Work Summary")

    header_bg = "#1e88e5"
    header_fg = "white"
    row_bg = "#ffffff"

    summary_frame = ttk.Frame(root, padding=10)
    summary_frame.grid(row=0, column=0, sticky="NSEW")

    # Header labels
    tk.Label(
        summary_frame,
        text="Employee",
        font=("Segoe UI", 10, "bold"),
        bg=header_bg,
        fg=header_fg,
        padx=10,
        pady=5,
        relief="ridge",
        bd=2,
    ).grid(row=0, column=0, sticky="NSEW")

    tk.Label(
        summary_frame,
        text="Shifts Assigned",
        font=("Segoe UI", 10, "bold"),
        bg=header_bg,
        fg=header_fg,
        padx=10,
        pady=5,
        relief="ridge",
        bd=2,
    ).grid(row=0, column=1, sticky="NSEW")

    # Employee data rows
    for row, (emp, count) in enumerate(sorted(employee_work_days.items()), start=1):
        tk.Label(
            summary_frame,
            text=emp,
            font=("Segoe UI", 10),
            bg=row_bg,
            padx=10,
            pady=5,
            relief="solid",
            bd=1,
        ).grid(row=row, column=0, sticky="NSEW")

        tk.Label(
            summary_frame,
            text=str(count),
            font=("Segoe UI", 10),
            bg=row_bg,
            padx=10,
            pady=5,
            relief="solid",
            bd=1,
        ).grid(row=row, column=1, sticky="NSEW")

    # Grid expansion
    summary_frame.columnconfigure(0, weight=1)
    summary_frame.columnconfigure(1, weight=1)

    root.mainloop()


# --- Example Usage ---
if __name__ == "__main__":
    # Each employee has preferences for each day. If a day is not listed, they have no preference.
    # Preferences are lists, indicating priority.
    sample_employee_preferences = {
        "Ricky": {
            "Monday": ["Afternoon", "Evening"],
            "Tuesday": ["Evening", "Morning"],
            "Thursday": ["Morning"],
            "Friday": ["Morning"],
        },
        "John": {
            "Tuesday": ["Morning"],
            "Wednesday": ["Morning"],
            "Thursday": ["Morning"],
            "Friday": ["Morning"],
            "Saturday": ["Morning"],
            "Sunday": ["Morning"],
        },
        "Nuguid": {
            "Monday": ["Evening"],
            "Tuesday": ["Evening"],
            "Wednesday": ["Evening"],
            "Thursday": ["Evening"],
            "Friday": ["Evening"],
            "Saturday": ["Evening"],
        },
        "Elyza": {
            "Monday": ["Evening", "Morning"],
            "Tuesday": ["Morning"],
            "Wednesday": ["Evening"],
            "Thursday": ["Afternoon"],
            "Friday": ["Morning"],
            "Saturday": ["Afternoon"],
            "Sunday": ["Morning"],
        },
        "Allison": {
            "Monday": ["Morning", "Evening"],
            "Tuesday": ["Afternoon"],
            "Wednesday": ["Morning"],
            "Thursday": ["Afternoon"],
            "Friday": ["Evening"],
            "Saturday": ["Evening"],
            "Sunday": ["Afternoon"],
        },
        "Henry": {
            "Monday": ["Afternoon"],
            "Tuesday": ["Evening"],
            "Wednesday": ["Afternoon"],
            "Thursday": ["Evening"],
            "Friday": ["Morning"],
            "Saturday": ["Morning"],
            "Sunday": ["Evening"],
        },
        "Cavil": {
            "Monday": ["Evening"],
            "Tuesday": ["Morning"],
            "Wednesday": ["Morning"],
            "Thursday": ["Morning", "Evening"],
            "Friday": ["Afternoon", "Evening"],
            "Saturday": ["Afternoon", "Evening"],
            "Sunday": ["Morning", "Evening"],
        },
        # No preferences at all
        "Merit": {},
        "Braxton": {},
        "Neil": {},
        "Marko": {},
    }

    # 2. Scheduling Logic (called by create_schedule function)
    # 3. Shift Conflicts (handled within create_schedule, prioritizing same-day alternatives
    #    based on preference order and then random assignment for minimums)
    final_schedule, employee_days, unassigned = create_schedule(
        sample_employee_preferences
    )

    # 4. Output: Display the final schedule
    display_schedule(final_schedule, employee_days)

    # Graphical Display of schdule and the number of shifts assigned to each employee
    display_schedule_ui(final_schedule)
    display_employee_summary_ui(employee_days)

    # Output any employees who couldn't be assigned at all
    if unassigned:
        print(
            "\nNote: The following employees were not assigned for some days due to conflicts or limits:"
        )
        for emp in unassigned:
            print(f"- {emp}")
