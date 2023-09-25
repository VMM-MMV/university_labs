import java.util.Objects;
import java.util.Scanner;

public class MainApp {
    public MainApp() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter something:");
        String userInput = scanner.nextLine();

        if (Objects.equals(userInput, "f")) {
            FacultyOperations facultyOperations = new FacultyOperations();
        } else if (Objects.equals(userInput, "g")) {
            GeneralOperations generalOperations = new GeneralOperations();
        } else{
            System.out.println("No such command");
        }
    }
}
