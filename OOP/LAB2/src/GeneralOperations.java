import java.util.Objects;
import java.util.Scanner;

public class GeneralOperations {
        public GeneralOperations() {
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
                case "nf" -> newFaculty();
                case "ss" -> searchStudent();
                case "df" -> displayFaculties();
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

