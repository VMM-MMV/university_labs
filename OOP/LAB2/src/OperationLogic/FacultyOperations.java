package OperationLogic;

import Faculties.Faculty;
import Faculties.GraduatedFromFaculty;
import Faculties.StudentFaculty;
import Templates.Student;
import org.jetbrains.annotations.Contract;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;



public class FacultyOperations extends Storage {
    private static FacultyOperations instance;

    private FacultyOperations() {
    }

    public static FacultyOperations getInstance() {
        if (instance == null) {
            instance = new FacultyOperations();
        }
        return instance;
    }

    public static void startOperations() {
        var scanner = new Scanner(System.in);
        String result;


        System.out.println("F: Enter command:");
        String userInput = scanner.nextLine();


        result = checkInput(userInput);

        FacultyOperations.getInstance();
    }

    private static @NotNull String checkInput(String userInput) {
        if (userInput.length() < 2) {
            System.out.println("String is too short!");
            return "";
        }

        if (userInput.equals("help")) {
            System.out.println("""
                Faculties.Faculty operations
                
                ns/<faculty abbreviation>/<firstName>/<LastName>/<email>/<day>/<month>/<year> - create student
                gs/<email> - (g)raduate (s)tudent
                de/<faculty abbreviation> - (d)isplay enrolled (s)tudents
                dg/<faculty abbreviation> - (d)isplay (g)raduated students
                bf/<faculty abbreviation>/<email> - check if student (b)elongs to (f)aculty
                
                bk - Back
                br - Exit and Save""");
            startOperations();
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

        if (parts.length < 7) {
            System.out.println("Incomplete command operation.");
            return;
        }

        String facultyAbbreviation = parts[1];

        if (!doesFacultyExist(facultyAbbreviation, Storage.studentFaculties)) {
            System.out.println("Faculties.Faculty Does Not Exist");
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

        for (StudentFaculty studentFaculty : Storage.studentFaculties) {
            if (Objects.equals(facultyAbbreviation, studentFaculty.getAbbreviation())) {
                studentFaculty.addStudent(new Student(firstName, lastName, email, enrollmentDate, dateOfBirth));
                return;
            }
        }
    }
    // nf/fcimbig/fcim/URBANISM_ARCHITECTURE

    // ns/fcim/mihai/vieru/viem2377@gmail.com/01-09-2022/07-07-2003

    // gs/viem2377@gmail.com

    private static void graduateStudent(@NotNull String commandOperation) {
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
        if(!doesFacultyExist(studentFaculty.getAbbreviation(), Storage.graduatedFromFaculties)){
            GraduatedFromFaculty graduatedFromFaculty = createFacultyForGraduates(studentFaculty);
            Storage.graduatedFromFaculties.add(graduatedFromFaculty);
        }

        // Add User To GraduatedFaculty
        for (GraduatedFromFaculty graduatedFromFaculty : Storage.graduatedFromFaculties) {
            if (Objects.equals(graduatedFromFaculty.getAbbreviation(), studentFaculty.getAbbreviation())) {
                graduatedFromFaculty.addStudent(student);
            }
        }

        // Remove Templates.Student From Faculties.StudentFaculty
        studentFaculty.removeStudent(student);
    }


    private static void displayEnrolled() {
        if(Storage.studentFaculties != null) {
            for (StudentFaculty studentFaculty : Storage.studentFaculties) {
                System.out.println("Faculties.Faculty: " + studentFaculty.getName());
                for (Student student : studentFaculty.getStudents()) {
                    System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
                }
            }
        } else {System.out.println("Initialize a faculty");}
    }

    private static void displayGraduated() {
        if(Storage.graduatedFromFaculties != null) {
            for (GraduatedFromFaculty graduatedFromFaculty : Storage.graduatedFromFaculties) {
                System.out.println("Faculties.Faculty: " + graduatedFromFaculty.getName());
                for (Student student : graduatedFromFaculty.getStudents()) {
                    System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
                }
            }
        } else {System.out.println("Initialize a faculty");}
    }

    private static void belongsToFaculty(@NotNull String commandOperation) {
        var parts = commandOperation.split("/");
        if (parts.length < 3) {
            System.out.println("Incomplete command operation.");
            return;
        }
        String facultyAbbreviation = parts[1];
        String studentEmail = parts[2];

        if(Storage.studentFaculties != null) {
            for (StudentFaculty studentFaculty : Storage.studentFaculties) {
                if (Objects.equals(studentFaculty.getAbbreviation(), facultyAbbreviation)) {
                    for (Student student : studentFaculty.getStudents()) {
                        if (Objects.equals(student.getEmail(), studentEmail)) {
                            System.out.println("Templates.Student is present in facility.");
                            return;
                        }
                    }
                }
            }
        } else {System.out.println("Initialize a faculty");}
        System.out.println("Templates.Student is not present in facility.");
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

    @Contract("!null -> new")
    private static @Nullable GraduatedFromFaculty createFacultyForGraduates(StudentFaculty studentFaculty) {
        if(studentFaculty != null) {
            String facultyName =  studentFaculty.getName();
            String facultyAbbreviation =  studentFaculty.getAbbreviation();
            var facultyStudyField =  studentFaculty.getStudyField();
            return new GraduatedFromFaculty(facultyName, facultyAbbreviation, new ArrayList<>(), facultyStudyField);
        } else {System.out.println("Initialize a faculty");}
        return null;
    }

    public static @Nullable Map<StudentFaculty, Student> findStudentInFaculty(String studentEmail) {
        if(Storage.studentFaculties != null) {
            for (StudentFaculty studentFaculty : Storage.studentFaculties) {

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
        } else {System.out.println("Initialize a faculty");}
        return null;
    }
}
