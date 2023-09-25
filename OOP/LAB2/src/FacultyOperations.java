import org.jetbrains.annotations.NotNull;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Objects;
import java.util.Scanner;

public class FacultyOperations extends Operations {

    static void startOperations() {
        Scanner scanner = new Scanner(System.in);
        String result;

        do {
            System.out.println("F: Enter command:");
            String userInput = scanner.nextLine();

            result = checkInput(userInput);
        } while (!result.equals("bk") && !result.equals("br"));

        if (result.equals("br")) { return; }

        MainApp.mainMenu();
    }

    private static @NotNull String checkInput(@NotNull String userInput) {
        if (userInput.length() < 2) {
            System.out.println("String is too short!");
            return "";
        }

        String commandCall = userInput.substring(0, 2);
        String commandOperation = userInput.substring(2);

        switch (Objects.requireNonNull(commandCall)) {
            case "ns" -> newStudent(commandOperation);
            case "gs" -> graduateStudent(commandOperation);
            case "de" -> displayEnrolled();
            case "dg" -> displayGraduated();
            case "bf" -> belongsToFaculty(commandOperation);
            case "br" -> { return "br"; }
            case "bk" -> { return "bk"; }
            default -> System.out.println("No such command");
        }
        return "";
    }

    private static void newStudent(String commandOperation) {
        String[] parts = commandOperation.split("/");
        String FacultyAbbreviation = parts[1];

        String firstName = parts[2];
        String lastName = parts[3];
        String email = parts[4];
        SimpleDateFormat dateFormat = new SimpleDateFormat("dd-MM-yyyy");
        Date enrollmentDate;
        Date dateOfBirth;

        try {
            enrollmentDate = dateFormat.parse(parts[5]);
            dateOfBirth = dateFormat.parse(parts[6]);
        } catch (ParseException e) {
            e.printStackTrace();
            System.out.println("Error parsing date");
            return;
        }

        for (StudentFaculty studentFaculty : studentFaculties) {
            if (Objects.equals(FacultyAbbreviation, studentFaculty.getAbbreviation())) {
                Student newStudent = new Student(firstName, lastName, email, enrollmentDate, dateOfBirth);
                studentFaculty.addStudent(newStudent);
                System.out.println("Student added: " + newStudent.getFirstName() + " " + newStudent.getLastName());
                System.out.println("Student added to " + studentFaculty.getName());
                System.out.println("Student added to " + studentFaculty.getName());
//                return;
            }
        }

        for (Faculty faculty : studentFaculties) {
            System.out.println("Faculty: " + faculty.getName());
            for (Student student : faculty.getStudents()) {
                System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
            }
        }
    }
    // nf/fcimbig/fcim/URBANISM_ARCHITECTURE

    // ns/fcim/mihai/vieru/viem2377@gmail.com/01-09-2022/07-07-2003

    private static void graduateStudent(String commandOperation) {
        System.out.println("graduateStudent");
    }

    private static void displayEnrolled() {


    }

    private static void displayGraduated() {
        System.out.println("displayGraduated");
    }

    private static void belongsToFaculty(String commandOperation) {
        System.out.println("belongsToFaculty");
    }


}
