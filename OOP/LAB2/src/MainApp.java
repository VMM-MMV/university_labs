import java.util.Objects;
import java.util.Scanner;

public class MainApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter something:");
        String userInput = scanner.nextLine();

        System.out.println(userInput);
        if (Objects.equals(userInput, "f")) {
            FacultyOperations facultyOperations = new FacultyOperations();
        } else if (Objects.equals(userInput, "g")) {
            GeneralOperations generalOperations = new GeneralOperations();
        }
    }
}
