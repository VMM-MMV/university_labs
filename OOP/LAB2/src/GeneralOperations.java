import java.util.Objects;
import java.util.Scanner;

public class GeneralOperations {
    static void startOperations() {
        Scanner scanner = new Scanner(System.in);
        String result;

        do {
            System.out.println("G: Enter command:");
            String userInput = scanner.nextLine();

            result = checkInput(userInput);
        } while (!result.equals("bk") && !result.equals("br"));

        if (result.equals("br")) { return; }

        MainApp.mainMenu();
    }

    private static String checkInput(String userInput) {
        if (userInput.length() < 2) {
            System.out.println("String is too short!");
            return "";
        }

        String command = userInput.substring(0, 2);

        switch (Objects.requireNonNull(command)) {
            case "nf" -> newFaculty();
            case "ss" -> searchStudent();
            case "df" -> displayFaculties();
            case "br" -> { return "br"; }
            case "bk" -> { return "bk"; }
            default -> System.out.println("No such command");
        }
        return "";
    }

    private static void newFaculty() {
        System.out.println("newFaculty");
    }

    private static void searchStudent() {
        System.out.println("searchStudent");
    }

    private static void displayFaculties() {
        System.out.println("displayFaculties");
    }
}
