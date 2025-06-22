import java.util.*;

public class EmployeeShifts {
    // Constants for scheduling rules
    static final int MAX_DAYS = 5;
    static final int MIN_EMPLOYEES = 2;

    // Enum for days of the week
    enum DayOfWeek {
        SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY
    }

    // Enum for shift types
    enum ShiftType {
        MORNING, AFTERNOON, EVENING
    }

    // Static Employee class to represent each employee
    static class Employee {
        // Name of the employee
        String name;

        // Store Day preferences for Employee
        Map<DayOfWeek, ShiftType> preferredShifts;

        // How many days employee has worked this week
        int daysWorkedThisWeek;

        // Helper to flag if employee has a shift today
        boolean hasShiftToday;

        // Contructor to initialize an employee with a name and empty preferences
        public Employee(String name) {
            this.name = name;
            this.preferredShifts = new HashMap<>();
            this.daysWorkedThisWeek = 0;
            this.hasShiftToday = false;
        }

        // Getters for employee properties
        public String getName() {
            return name;
        }

        public Map<DayOfWeek, ShiftType> getPreferredShifts() {
            return preferredShifts;
        }

        public int getDaysWorkedThisWeek() {
            return daysWorkedThisWeek;
        }

        public void incrementDaysWorked() {
            this.daysWorkedThisWeek++;
        }

        public boolean hasShiftToday() {
            return hasShiftToday;
        }

        public void setHasShiftToday(boolean hasShiftToday) {
            this.hasShiftToday = hasShiftToday;
        }

        @Override
        public String toString() {
            return name;
        }
    }

    // Weekly company schedule
    static Map<DayOfWeek, Map<ShiftType, List<Employee>>> weeklySchedule;

    // A list to store all registered employees
    static List<Employee> employees;

    public static void main(String[] args) {
        // Initialize data structures
        employees = new ArrayList<>();
        weeklySchedule = new EnumMap<>(DayOfWeek.class);

        // Initialize weekly schedule with empty lists for each day and shift
        for (DayOfWeek day : DayOfWeek.values()) {
            weeklySchedule.put(day, new EnumMap<>(ShiftType.class));
            for (ShiftType shift : ShiftType.values()) {
                weeklySchedule.get(day).put(shift, new ArrayList<>());
            }
        }

        // Test Employee Data
        System.out.println("--- Employees and their schedule preferences ---");
        // Calling Helper class to load employees
        // Switch between loading employees with or without preferences
        // loadEmployeesWithPreferences(employees);
        loadEmployeesWithoutPreferences(employees);

        System.out.println("\n--- Employee has been loaded  ---");
        System.out.println("\n--- Now Generating Schedule ---");

        // Looping through each day of the week to assign shifts
        for (DayOfWeek day : DayOfWeek.values()) {
            // Initailly resetting the entire employee's shift status for the day to false
            for (Employee emp : employees) {
                emp.setHasShiftToday(false);
            }

            // Begin scheduling for the current day
            System.out.println("\nScheduling Shifts for " + day + ":");

            // Based on employee preferences, assign shifts
            for (Employee emp : employees) {
                // If the employee has worked less than 5 days this week and doesn't have a
                // shift
                if (emp.getDaysWorkedThisWeek() < MAX_DAYS && !emp.hasShiftToday()) {
                    // Does the employee have a preferred shift for this day?
                    ShiftType preferredShift = emp.getPreferredShifts().get(day);
                    // If they do, try to assign them to that shift
                    if (preferredShift != null) {
                        List<Employee> shiftEmployees = weeklySchedule.get(day).get(preferredShift);

                        // Initially load 2 people per each shift to fill all the calendar
                        if (shiftEmployees.size() < MIN_EMPLOYEES) {
                            shiftEmployees.add(emp);
                            emp.incrementDaysWorked();
                            emp.setHasShiftToday(true);
                            System.out.println(
                                    emp.getName() + " has been assigned to " + preferredShift + " shift.");
                        } else {
                            System.out.println(emp.getName() + "'s preferred " + preferredShift
                                    + " has been filled for " + day + ".");
                            // Check if the employee can be assigned to another shift
                            assignAlternateShift(emp, day);
                        }
                    }
                    // If the employee has worked 5 days, skip them
                } else if (emp.getDaysWorkedThisWeek() >= MAX_DAYS) {
                    System.out.println(emp.getName() + " has worked for the maximum days this week ("
                            + emp.getDaysWorkedThisWeek() + ").");
                }
            }

            Random random = new Random();

            // If the preferred shifts are not filled, try to fill them with unassigned
            // employees
            for (ShiftType shift : ShiftType.values()) {
                // Get the current list of employees assigned to this shift
                List<Employee> currentShiftEmployees = weeklySchedule.get(day).get(shift);

                // Making sure each shift has at least 2 employees
                while (currentShiftEmployees.size() < MIN_EMPLOYEES) {
                    System.out.println(shift + " shift for " + day + " has not met the minimum employee count ("
                            + currentShiftEmployees.size() + ").");
                    // Finding employees who have not been assigned today and have worked less than
                    // 5 days
                    Employee assignedFiller = null;
                    List<Employee> availableFillers = new ArrayList<>();
                    for (Employee emp : employees) {
                        if (emp.getDaysWorkedThisWeek() < MAX_DAYS && !emp.hasShiftToday()) {
                            availableFillers.add(emp);
                        }
                    }

                    // If there are available employees to fill the shift
                    if (!availableFillers.isEmpty()) {
                        // Randomly select an employee from the available fillers
                        assignedFiller = availableFillers.get(random.nextInt(availableFillers.size()));
                        currentShiftEmployees.add(assignedFiller);
                        assignedFiller.incrementDaysWorked();
                        assignedFiller.setHasShiftToday(true);
                        System.out.println(
                                assignedFiller.getName() + " has been assigned to " + shift + " shift.");
                    } else {
                        System.out.println(
                                "No additional employees is available to fill " + shift + " shift for " + day
                                        + ".");
                        break;
                    }
                }
            }
        }

        // Now that the schedule is generated, print the final weekly schedule
        System.out.println("\n--- Weekly Employee Shift Schedule ---");

        // Loop through each day of the week and print the assigned employees for each
        for (DayOfWeek day : DayOfWeek.values()) {
            System.out.println("\n" + day + ":");
            for (ShiftType shift : ShiftType.values()) {
                List<Employee> assignedEmployees = weeklySchedule.get(day).get(shift);
                System.out.print("  " + shift + ": ");
                // If the list is empty, no employees assigned
                if (assignedEmployees.isEmpty()) {
                    System.out.println("No employees assigned.");
                } else {
                    // Print he names of assigned employees
                    for (int i = 0; i < assignedEmployees.size(); i++) {
                        System.out.print(assignedEmployees.get(i).getName());
                        if (i < assignedEmployees.size() - 1) {
                            System.out.print(", ");
                        }
                    }
                    System.out.println("(Total: " + assignedEmployees.size() + ")");
                }
            }
        }

        System.out.println("\n--- Employee total shifts summary ---");
        for (Employee emp : employees) {
            System.out.println(emp.getName() + " worked " + emp.getDaysWorkedThisWeek() + " days.");
        }
    }

    // Sheduling employee for alternate shifts if their preferred shift is full
    private static void assignAlternateShift(Employee emp, DayOfWeek day) {
        ShiftType[] shiftsToTry = ShiftType.values();

        for (ShiftType altShift : shiftsToTry) {
            // Skip preferred shift
            if (emp.getPreferredShifts().get(day) != null && emp.getPreferredShifts().get(day) == altShift) {
                continue;
            }

            List<Employee> altShiftEmployees = weeklySchedule.get(day).get(altShift);

            // Only if the alternate shift has less than the minimum employees
            if (altShiftEmployees.size() < MIN_EMPLOYEES && !emp.hasShiftToday()) {
                altShiftEmployees.add(emp);
                emp.incrementDaysWorked();
                emp.setHasShiftToday(true);
                System.out.println("Employee : " + emp.getName() + " assigned to " + altShift + " shift on "
                        + day + ".");
                return;
            }
        }

        // If no alternate shift could be assigned
        System.out.println(emp.getName() + " cannot be assigned to alternate shift on " + day
                + " (all full or already assigned).");
    }

    // Helper Class to load employees
    static void loadEmployeesWithoutPreferences(List<Employee> employees) {
        employees.add(new Employee("Mary"));
        employees.add(new Employee("Kate"));
        employees.add(new Employee("Kevin"));
        employees.add(new Employee("Patrick"));
        employees.add(new Employee("Evan"));
        employees.add(new Employee("Joe"));
    }

    static void loadEmployeesWithPreferences(List<Employee> employees) {
        // Employee List Initialization
        Employee emp1 = new Employee("Mary");
        emp1.getPreferredShifts().put(DayOfWeek.MONDAY, ShiftType.MORNING);
        emp1.getPreferredShifts().put(DayOfWeek.TUESDAY, ShiftType.MORNING);
        emp1.getPreferredShifts().put(DayOfWeek.WEDNESDAY, ShiftType.MORNING);
        employees.add(emp1);

        Employee emp2 = new Employee("Kate");
        emp2.getPreferredShifts().put(DayOfWeek.WEDNESDAY, ShiftType.EVENING);
        emp2.getPreferredShifts().put(DayOfWeek.FRIDAY, ShiftType.EVENING);
        emp2.getPreferredShifts().put(DayOfWeek.SATURDAY, ShiftType.EVENING);
        employees.add(emp2);

        Employee emp3 = new Employee("Kevin");
        emp3.getPreferredShifts().put(DayOfWeek.TUESDAY, ShiftType.AFTERNOON);
        emp3.getPreferredShifts().put(DayOfWeek.WEDNESDAY, ShiftType.AFTERNOON);
        emp3.getPreferredShifts().put(DayOfWeek.THURSDAY, ShiftType.AFTERNOON);
        emp3.getPreferredShifts().put(DayOfWeek.SATURDAY, ShiftType.AFTERNOON);
        emp3.getPreferredShifts().put(DayOfWeek.SUNDAY, ShiftType.AFTERNOON);
        employees.add(emp3);

        Employee emp4 = new Employee("Patrick");
        emp4.getPreferredShifts().put(DayOfWeek.MONDAY, ShiftType.MORNING);
        emp4.getPreferredShifts().put(DayOfWeek.TUESDAY, ShiftType.MORNING);
        emp4.getPreferredShifts().put(DayOfWeek.WEDNESDAY, ShiftType.MORNING);
        emp4.getPreferredShifts().put(DayOfWeek.THURSDAY, ShiftType.MORNING);
        emp4.getPreferredShifts().put(DayOfWeek.FRIDAY, ShiftType.MORNING);
        emp4.getPreferredShifts().put(DayOfWeek.SATURDAY, ShiftType.MORNING);
        emp4.getPreferredShifts().put(DayOfWeek.SUNDAY, ShiftType.MORNING);
        employees.add(emp4);

        Employee emp5 = new Employee("Evan");
        emp5.getPreferredShifts().put(DayOfWeek.MONDAY, ShiftType.EVENING);
        emp5.getPreferredShifts().put(DayOfWeek.TUESDAY, ShiftType.MORNING);
        emp5.getPreferredShifts().put(DayOfWeek.WEDNESDAY, ShiftType.EVENING);
        emp5.getPreferredShifts().put(DayOfWeek.THURSDAY, ShiftType.AFTERNOON);
        emp5.getPreferredShifts().put(DayOfWeek.FRIDAY, ShiftType.EVENING);
        employees.add(emp5);

        Employee emp6 = new Employee("Joe");
        employees.add(emp6);

        Employee emp7 = new Employee("Terril");
        employees.add(emp7);

        Employee emp8 = new Employee("Nancy");
        employees.add(emp8);
    }
}