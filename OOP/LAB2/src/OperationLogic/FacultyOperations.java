package OperationLogic;

import DataBase.FileManager;
import Logging.Logger;
import Templates.Faculty;
import Templates.Student;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

import static OperationLogic.UserInput.scanner;

public class FacultyOperations {
    static Logger logger = new Logger("FacultyLogs.log");
    public void startOperations() {
        String result;
        String userInput;
        do {
            System.out.println("F: Enter command:");
            userInput = scanner.nextLine();

            result = doOperations(userInput);
        } while (!result.equals("bk"));
    }

    private String doOperations(String userInput) {
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
            case "br" -> { FileManager.saveData(); System.exit(0); }
            case "bk" -> { return "bk"; }
            case "dh" -> displayHelp();
            case "ms" -> massOperations("newStudents", commandOperation);
            case "mg" -> massOperations("graduateStudents", commandOperation);
            default -> System.out.println("No such command");
        }
        return "";
    }

    private static void newStudent(String commandOperation) {
        var parts = commandOperation.split("/");

        if (parts.length < 7) {
            System.out.println("Incomplete command operation.");
            return;
        }

        String facultyAbbreviation = parts[1];

        if (!doesFacultyExist(facultyAbbreviation, Storage.getAllFacultiesList())) {
            System.out.println("Faculty Does Not Exist");
            return;
        }

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

        for (Faculty faculty : Storage.getAllFacultiesList()) {
            if (Objects.equals(facultyAbbreviation, faculty.getAbbreviation())) {
                faculty.addStudent(new Student(firstName, lastName, email, enrollmentDate, dateOfBirth, StudentRole.NOT_GRADUATED));
                logger.log("New student: " + firstName + " " + lastName);
                return;
            }
        }
    }
    // nf/fcimbig/fcim/URBANISM_ARCHITECTURE

    // ns/fcim/mihai/vieru/viem2377@gmail.com/01-09-2022/07-07-2003

    // gs/viem2377@gmail.com

    private static void graduateStudent(String commandOperation) {
        var parts = commandOperation.split("/");
        if (parts.length < 2) {
            System.out.println("Incomplete command operation.");
            return;
        }

        String studentEmail = parts[1];

        for (Faculty faculty : Storage.getAllFacultiesList()) {
            for (Student student : faculty.getStudents()) {
                if (Objects.equals(studentEmail, student.getEmail()) && student.getStudentRole() == StudentRole.NOT_GRADUATED) {
                    student.setStudentRole(StudentRole.GRADUATED);
                    logger.log(student + " Has Been Graduated");
                    return;
                }
            }
        }
        System.out.println("Student is not enrolled");
    }

    private void displayEnrolled() {
        for (Faculty faculty : Storage.getAllFacultiesList()) {
            System.out.println("Faculty: " + faculty.getName());
            for (Student student : faculty.getStudents()) {
                if (student.getStudentRole() == StudentRole.NOT_GRADUATED) {
                    System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
                }
            }
        }
    }

    private void displayGraduated() {
        for (Faculty faculty : Storage.getAllFacultiesList()) {
            System.out.println("Faculty: " + faculty.getName());
            for (Student student : faculty.getStudents()) {
                if (student.getStudentRole() == StudentRole.GRADUATED) {
                    System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
                }
            }
        }
    }

    private void belongsToFaculty(String commandOperation) {
        var parts = commandOperation.split("/");
        if (parts.length < 3) {
            System.out.println("Incomplete command operation.");
            return;
        }

        String facultyAbbreviation = parts[1];
        String studentEmail = parts[2];


        for (Faculty faculty : Storage.getAllFacultiesList()) {
            if (Objects.equals(faculty.getAbbreviation(), facultyAbbreviation)) {
                for (Student student : faculty.getStudents()) {
                    if (Objects.equals(student.getEmail(), studentEmail) && student.getStudentRole() == StudentRole.NOT_GRADUATED) {
                        System.out.println("Student is present in faculty.");
                        return;
                    }
                }
            }
        }
        System.out.println("Student is not present in faculty.");
    }

    private static boolean doesFacultyExist(String abbreviation, ArrayList<Faculty> faculties) {
        for (Faculty faculty : faculties) {
            if (Objects.equals(abbreviation, faculty.getAbbreviation())) {
                return true;
            }
        }
        return false;
    }

    private void displayHelp() {
        System.out.println("""
                Faculty operations
                
                ns/<faculty abbreviation>/<firstName>/<LastName>/<email>/<day>/<month>/<year>/<day>/<month>/<year> - create student
                gs/<email> - (g)raduate (s)tudent
                de/<faculty abbreviation> - (d)isplay enrolled (s)tudents
                dg/<faculty abbreviation> - (d)isplay (g)raduated students
                bf/<faculty abbreviation>/<email> - check if student (b)elongs to (f)aculty
                ms/<file path> - (m)ass add (s)tudents
                mg/<file path> - (m)ass (g)raduate students
                
                bk - (b)ac(k)
                br - exit and save
                dh - (d)isplay (h)elp""");
    }

    private void massOperations(String operation, String commandOperation) {
        var index = commandOperation.indexOf("/");
        var filePath = commandOperation.substring(index + 1);

        try (BufferedReader bufferedReader = new BufferedReader(new FileReader(filePath))) {

            String line;
            logger.log("Start Mass Operation: ");
            while ((line = bufferedReader.readLine()) != null) {
                switch (operation) {
                    case "newStudents" -> newStudent(line);
                    case "graduateStudents" -> graduateStudent(line);
                    default -> System.out.println("Invalid mass operation");
                }
            }
            logger.log("End Mass Operation: ");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}