import java.util.Objects;
import java.util.Scanner;

public class FacultyOperations {

    public FacultyOperations() {
        startOperations();
    }

    private void startOperations() {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("F: Enter command:");
            String userInput = scanner.nextLine();
            if ("br".equalsIgnoreCase(userInput)) {
                break;
            }
            checkInput(userInput);
        }
    }

    private void checkInput(String userInput) {
        if (userInput.length() < 2) {
            System.out.println("String is too short!");
            return;
        }

        String command = userInput.substring(0, 2);

        switch (Objects.requireNonNull(command)) {
            case "ns" -> newStudent();
            case "gs" -> graduateStudent();
            case "de" -> displayEnrolled();
            case "dg" -> displayGraduated();
            case "bf" -> belongsToFaculty();
            case "bk" -> new MainApp();
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
