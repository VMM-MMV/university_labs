import java.util.Objects;
import java.util.Scanner;

public class FacultyOperations {

    static void startOperations() {
        Scanner scanner = new Scanner(System.in);
        String result = null;
        while (true) {
            System.out.println("F: Enter command:");
            String userInput = scanner.nextLine();

            result = checkInput(userInput);
            if(result.equals("bk") || result.equals("br")){
                break;
            }
        }
        if (result.equals("br")) {return;}
        MainApp.mainMenu();
    }

    private static String checkInput(String userInput) {
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
            case "br" -> { System.exit(0); }
            case "bk" -> { return "bk"; }
            default -> System.out.println("No such command");
        }
        return "";
    }

    private static void newStudent() {
        System.out.println("newStudent");
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
