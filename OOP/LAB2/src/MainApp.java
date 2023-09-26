import java.util.Objects;
import java.util.Scanner;

public class MainApp {
    public static void main(String[] args) {
        new LoadData();
        mainMenu();
    }

    public static void mainMenu() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter something:");
        String userInput = scanner.nextLine();

        switch (userInput) {
            case "f" -> FacultyOperations.startOperations();
            case "g" -> GeneralOperations.startOperations();
            case "br" -> new SaveData();
            case "help" -> { System.out.println("""
                    f - Go to Faculty Operations
                    g - Go to General Operations
                    
                    br - Exit and Save Program
                    """);
                mainMenu();
            }
            default -> {
                System.out.println("No such command");
                mainMenu();
            }
        }
    }
}
