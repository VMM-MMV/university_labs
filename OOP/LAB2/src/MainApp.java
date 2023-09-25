import java.util.Objects;
import java.util.Scanner;

public class MainApp {

    public static void main(String[] args) {
        mainMenu();
    }

    public static void mainMenu() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter something:");
        String userInput = scanner.nextLine();

        switch (userInput) {
            case "f" -> FacultyOperations.startOperations();
            case "g" -> GeneralOperations.startOperations();
            case "br" -> {return;}
            default -> {
                System.out.println("No such command");
                mainMenu();
            }
        }

    }
}
