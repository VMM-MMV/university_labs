import org.jetbrains.annotations.NotNull;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class FacultyOperations extends Operations {

    static void startOperations() {
        var scanner = new Scanner(System.in);
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
        var parts = commandOperation.split("/");

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
        String studentEmail = parts[1];
        Map<StudentFaculty, Student> studentMap = findStudentInFaculty(studentEmail);

        StudentFaculty faculty;
        Student student;

        if(studentMap != null && !studentMap.isEmpty()) {
            Map.Entry<StudentFaculty, Student> entry = studentMap.entrySet().iterator().next();
            faculty = entry.getKey();
            student = entry.getValue();
        } else {
            System.out.println("No student found with the given email.");
            return;
        }

        // Create GraduatedFaculty if it does not exist
        if(!doesFacultyExist(faculty.getAbbreviation(), graduatedFromFaculties)){
            GraduatedFromFaculty graduatedFromFaculty = createFacultyForGraduates(faculty);
            graduatedFromFaculties.add(graduatedFromFaculty);
        }

        // Add User To GraduatedFaculty
        for (GraduatedFromFaculty graduatedFromFaculty : graduatedFromFaculties) {
            if (Objects.equals(graduatedFromFaculty.getAbbreviation(), faculty.getAbbreviation())) {
                graduatedFromFaculty.addStudent(student);
            }
        }

        // Remove Student From StudentFaculty
        faculty.removeStudent(student);
    }


    private static void displayEnrolled() {
        for (StudentFaculty faculty : studentFaculties) {
            System.out.println("Faculty: " + faculty.getName());
            for (Student student : faculty.getStudents()) {
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
        System.out.println("belongsToFaculty");
    }

    private static boolean doesFacultyExist(String abbreviation, ArrayList<? extends Faculty> faculties) {
        if(faculties != null) {
            for (Faculty faculty : faculties) {
                if (Objects.equals(abbreviation, faculty.getAbbreviation())) {
                    return true;
                }
            }
        } else {System.out.println("Initialize a faculty");}
        return false;
    }

    private static GraduatedFromFaculty createFacultyForGraduates(StudentFaculty studentFaculty) {
        String facultyName =  studentFaculty.getName();
        String facultyAbbreviation =  studentFaculty.getAbbreviation();
        var facultyStudyField =  studentFaculty.getStudyField();
        return new GraduatedFromFaculty(facultyName, facultyAbbreviation, new ArrayList<>(), facultyStudyField);
    }

    public static Map<StudentFaculty, Student> findStudentInFaculty(String studentEmail) {
        if(studentFaculties != null) {
            for (StudentFaculty faculty : studentFaculties) {

                if(faculty != null && faculty.getStudents() != null) {
                    for (Student student : faculty.getStudents()) {

                        if (student != null && Objects.equals(student.getEmail(), studentEmail)) {
                            Map<StudentFaculty, Student> result = new HashMap<>();
                            result.put(faculty, student);
                            return result;
                        }
                    }
                } else {System.out.println("Add students"); return null;}
            }
        } else {System.out.println("Initialize a faculty");}
        return null;
    }

}
