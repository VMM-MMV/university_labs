package OperationLogic;

import DataBase.SaveData;
import Faculties.Faculty;
import Faculties.GraduatedFromFaculty;
import Faculties.StudentFaculty;
import Templates.Student;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class FacultyOperations extends Storage {
    public static void startOperations() {
        String result;
        var scanner = new Scanner(System.in);
        String userInput;
        do {
            System.out.println("F: Enter command:");
            userInput = scanner.nextLine();

            result = doOperations(userInput);
        } while (!result.equals("bk"));

    }

    private static String doOperations(String userInput) {
        if(studentFaculties == null) {
            System.out.println("Initialize a faculty");
            return "";
        }

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
            case "br" -> { new SaveData(); System.exit(0); }
            case "bk" -> { return "bk"; }
            case "hp" -> printHelp();
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

        if (!doesFacultyExist(facultyAbbreviation, studentFaculties)) {
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

        for (StudentFaculty studentFaculty : studentFaculties) {
            if (Objects.equals(facultyAbbreviation, studentFaculty.getAbbreviation())) {
                studentFaculty.addStudent(new Student(firstName, lastName, email, enrollmentDate, dateOfBirth));
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
        Map<StudentFaculty, Student> studentMap = findStudentInFaculty(studentEmail);

        StudentFaculty studentFaculty;
        Student student;

        if(studentMap != null && !studentMap.isEmpty()) {
            Map.Entry<StudentFaculty, Student> entry = studentMap.entrySet().iterator().next();
            studentFaculty = entry.getKey();
            student = entry.getValue();
        } else {
            System.out.println("No student found with the given email.");
            return;
        }

        // Create GraduatedFaculty if it does not exist
        if(!doesFacultyExist(studentFaculty.getAbbreviation(), graduatedFromFaculties)){
            GraduatedFromFaculty graduatedFromFaculty = createFacultyForGraduates(studentFaculty);
            graduatedFromFaculties.add(graduatedFromFaculty);
        }

        // Add User To GraduatedFaculty
        for (GraduatedFromFaculty graduatedFromFaculty : graduatedFromFaculties) {
            if (Objects.equals(graduatedFromFaculty.getAbbreviation(), studentFaculty.getAbbreviation())) {
                graduatedFromFaculty.addStudent(student);
            }
        }

        // Remove Student From StudentFaculty
        studentFaculty.removeStudent(student);
    }


    private static void displayEnrolled() {
        for (StudentFaculty studentFaculty : studentFaculties) {
            System.out.println("Faculty: " + studentFaculty.getName());
            for (Student student : studentFaculty.getStudents()) {
                System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
            }
        }
    }

    private static void displayGraduated() {
        for (GraduatedFromFaculty graduatedFromFaculty : graduatedFromFaculties) {
            System.out.println("Faculty: " + graduatedFromFaculty.getName());
            for (Student student : graduatedFromFaculty.getStudents()) {
                System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
            }
        }
    }

    private static void belongsToFaculty(String commandOperation) {
        var parts = commandOperation.split("/");
        if (parts.length < 3) {
            System.out.println("Incomplete command operation.");
            return;
        }
        String facultyAbbreviation = parts[1];
        String studentEmail = parts[2];


        for (StudentFaculty studentFaculty : studentFaculties) {
            if (Objects.equals(studentFaculty.getAbbreviation(), facultyAbbreviation)) {
                for (Student student : studentFaculty.getStudents()) {
                    if (Objects.equals(student.getEmail(), studentEmail)) {
                        System.out.println("Student is present in facility.");
                        return;
                    }
                }
            } else {System.out.println("Initialize a faculty");}
        }
        System.out.println("Student is not present in facility.");
    }

    private static boolean doesFacultyExist(String abbreviation, ArrayList<? extends Faculty> faculties) {
        for (Faculty faculty : faculties) {
            if (Objects.equals(abbreviation, faculty.getAbbreviation())) {
                return true;
            }
        }
        return false;
    }

    private static GraduatedFromFaculty createFacultyForGraduates(StudentFaculty studentFaculty) {
        String facultyName =  studentFaculty.getName();
        String facultyAbbreviation =  studentFaculty.getAbbreviation();
        var facultyStudyField =  studentFaculty.getStudyField();
        return new GraduatedFromFaculty(facultyName, facultyAbbreviation, new ArrayList<>(), facultyStudyField);
    }

    public static Map<StudentFaculty, Student> findStudentInFaculty(String studentEmail) {
        for (StudentFaculty studentFaculty : studentFaculties) {

            if(studentFaculty != null && studentFaculty.getStudents() != null) {
                for (Student student : studentFaculty.getStudents()) {

                    if (Objects.equals(student.getEmail(), studentEmail)) {
                        Map<StudentFaculty, Student> result = new HashMap<>();
                        result.put(studentFaculty, student);
                        return result;
                    }
                }
            } else {System.out.println("Add students"); return null;}
        }
        return null;
    }

    public static void printHelp() {
        System.out.println("""
                Faculty operations
                
                ns/<faculty abbreviation>/<firstName>/<LastName>/<email>/<day>/<month>/<year> - create student
                gs/<email> - (g)raduate (s)tudent
                de/<faculty abbreviation> - (d)isplay enrolled (s)tudents
                dg/<faculty abbreviation> - (d)isplay (g)raduated students
                bf/<faculty abbreviation>/<email> - check if student (b)elongs to (f)aculty
                
                bk - Back
                br - Exit and Save""");
    }
}