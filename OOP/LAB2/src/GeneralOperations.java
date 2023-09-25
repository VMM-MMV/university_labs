import java.util.Objects;
import java.util.Scanner;

public class GeneralOperations {

    public GeneralOperations() {
        startOperations();
    }

    private void startOperations() {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("G: Enter command:");
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
            case "nf" -> newFaculty();
            case "ss" -> searchStudent();
            case "df" -> displayFaculties();
            case "bk" -> new MainApp();
            default -> System.out.println("No such command");
        }
    }

    private void newFaculty() {
        System.out.println("newFaculty");
    }

    private void searchStudent() {
        System.out.println("searchStudent");
    }

    private void displayFaculties() {
        System.out.println("displayFaculties");
    }
}
