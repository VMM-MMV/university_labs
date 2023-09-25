import java.util.Objects;
import java.util.Scanner;

public class FacultyOperations {
    public FacultyOperations() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter command:");
        String userInput = scanner.nextLine();
        checkInput(userInput);
    }
    private void checkInput(String userInput) {
        String command = null;
        if(userInput.length() >= 2) {
            command = userInput.substring(0, 2);
        } else {
            System.out.println("String is too short!");
        }

        switch (Objects.requireNonNull(command)) {
            case "ns" -> newStudent();
            case "gs" -> graduateStudent();
            case "de" -> displayEnrolled();
            case "dg" -> displayGraduated();
            case "bf" -> belongsToFaculty();
            default -> System.out.println("No such command");
        }
    }
    private void newStudent() {
        System.out.println("newStudent");

    }

    private void graduateStudent() {
        System.out.println("graduateStudent");

    }

    private void displayEnrolled() {
        System.out.println("displayEnrolled");
    }

    private void displayGraduated() {
        System.out.println("displayGraduated");

    }

    private void belongsToFaculty() {
        System.out.println("belongsToFaculty");

    }
}
