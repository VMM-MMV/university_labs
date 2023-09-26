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

        if (userInput.equals("help")) {
            System.out.println("""
                Faculty operations
                What do you want to do?
                
                ns/<faculty abbreviation>/<firstName>/<LastName>/<email>/<day>/<month>/<year> - create student
                gs/<email> - (g)raduate (s)tudent
                de/<faculty abbreviation> - (d)isplay enrolled (s)tudents
                dg/<faculty abbreviation> - (d)isplay (g)raduated students
                bf/<faculty abbreviation>/<email> - check if student (b)elongs to (f)aculty
                
                bk - Back
                br - Exit and Save""");
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
        if(studentFaculties != null) {
            for (StudentFaculty studentFaculty : studentFaculties) {
                System.out.println("Faculty: " + studentFaculty.getName());
                for (Student student : studentFaculty.getStudents()) {
                    System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
                }
            }
        } else {System.out.println("Initialize a faculty");}
    }

    private static void displayGraduated() {
        if(graduatedFromFaculties != null) {
            for (GraduatedFromFaculty graduatedFromFaculty : graduatedFromFaculties) {
                System.out.println("Faculty: " + graduatedFromFaculty.getName());
                for (Student student : graduatedFromFaculty.getStudents()) {
                    System.out.println("FirstName: " + student.getFirstName() + " | LastName: " + student.getLastName() + " | Email: " + student.getEmail() + " | DateOfBirth: " + student.getDateOfBirth() + " | EnrollmentDate: " + student.getEnrollmentDate());
                }
            }
        } else {System.out.println("Initialize a faculty");}
    }

    private static void belongsToFaculty(String commandOperation) {
        var parts = commandOperation.split("/");
        if (parts.length < 3) {
            System.out.println("Incomplete command operation.");
            return;
        }
        String facultyAbbreviation = parts[1];
        String studentEmail = parts[2];

        if(studentFaculties != null) {
            for (StudentFaculty studentFaculty : studentFaculties) {
                if (Objects.equals(studentFaculty.getAbbreviation(), facultyAbbreviation)) {
                    for (Student student : studentFaculty.getStudents()) {
                        if (Objects.equals(student.getEmail(), studentEmail)) {
                            System.out.println("Student is present in facility.");
                            return;
                        }
                    }
                }
            }
        } else {System.out.println("Initialize a faculty");}
        System.out.println("Student is not present in facility.");
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
        if(studentFaculty != null) {
            String facultyName =  studentFaculty.getName();
            String facultyAbbreviation =  studentFaculty.getAbbreviation();
            var facultyStudyField =  studentFaculty.getStudyField();
            return new GraduatedFromFaculty(facultyName, facultyAbbreviation, new ArrayList<>(), facultyStudyField);
        } else {System.out.println("Initialize a faculty");}
        return null;
    }

    public static Map<StudentFaculty, Student> findStudentInFaculty(String studentEmail) {
        if(studentFaculties != null) {
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
        } else {System.out.println("Initialize a faculty");}
        return null;
    }
}
