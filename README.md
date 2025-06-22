## Assignment Information

**Shrisan Kapali**  
**Student ID:** 005032249  
**Assignment 4:** Implementing Control Structures

---

## Overview

This repository contains two applications that manages employee shifts in a company. The project showcases the use of control structures such as loops, conditionals, and lists/maps to dynamically assign shifts based on available employee data and their preferences.

---

## Repository Contents

This repository contains two source files:

- **EmployeeShifts.java** – Java implementation of the shift assignment logic.
- **EmployeeShifts.py** – Python implementation of the shift assignment logic with sample data sets.

---

## Python Program: `EmployeeShifts.py`

The Python version demonstrates how to handle different scenarios using sample data sets. The `sample_employee_preferences` variable can be modified to test the application under different conditions.

### Included Data Sets:

1. **Empty Data Set:**

   - No employees present.
   - Used to test how the system behaves with no input.

2. **Employees Without Preferences:**

   - Employee names are provided, but no shift preferences are specified.

3. **Employees With Preferences:**

   - Both employee names and their preferred shifts are provided.

4. **Fewer Employees With and Without Preferences:**
   - A smaller group of employees is used for more edge-case testing, with a mix of those who have preferences and those who do not.

To switch between these data sets, simply change the value of the `sample_employee_preferences` variable at the beginning of the script.

---

## Java Program: `EmployeeShifts.java`

The Java implementation provides two helper functions:

- `loadEmployeesWithoutPreferences()`  
  Loads a list of employees without any shift preferences.

- `loadEmployeesWithPreferences()`  
  Loads a list of employees along with their shift preferences.

If employees are not loaded via either helper function, the system defaults to an empty employee list.

---

## Key Features

- Shift scheduling based on employee availability and preferences.
- Fallback logic for employees without preferences.
- Modular and extensible structure for testing different input configurations.
- Console output of assigned shifts and employee workload.

---

## How to Use

### Python:

1. Open `EmployeeShifts.py`
2. Modify the `sample_employee_preferences` variable to test different scenarios.
3. Run the script with Python.

### Java:

1. Open `EmployeeShifts.java`
2. Call either `loadEmployeesWithoutPreferences()` or `loadEmployeesWithPreferences()` in the `main()` function.
3. Compile and run the program.

---
