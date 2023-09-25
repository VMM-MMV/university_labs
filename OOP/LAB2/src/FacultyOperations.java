import org.jetbrains.annotations.NotNull;

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

        String command = userInput.substring(0, 2);

        switch (Objects.requireNonNull(command)) {
            case "ns" -> newStudent();
            case "gs" -> graduateStudent();
            case "de" -> displayEnrolled();
            case "dg" -> displayGraduated();
            case "bf" -> belongsToFaculty();
            case "br" -> { return "br"; }
            case "bk" -> { return "bk"; }
            default -> System.out.println("No such command");
        }
        return "";
    }

    private static void newStudent() {
    }

    private static void graduateStudent() {
        System.out.println("graduateStudent");
    }

    private static void displayEnrolled() {
        System.out.println("displayEnrolled");
    }

    private static void displayGraduated() {
        System.out.println("displayGraduated");
    }

    private static void belongsToFaculty() {
        System.out.println("belongsToFaculty");
    }
}
