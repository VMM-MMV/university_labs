import DataBase.FileManager;
import OperationLogic.FacultyOperations;
import OperationLogic.GeneralOperations;
import static OperationLogic.UserInput.scanner;

public class MainApp {
    public static void main(String[] args) {
        System.out.println("dh - DisplaysHelp");
        FileManager.loadData();
        mainMenu();
    }

    public static void mainMenu() {
        FacultyOperations facultyOperations = new FacultyOperations();
        GeneralOperations generalOperations = new GeneralOperations();
        String userInput;
        while(true) {

            System.out.println("Enter something:");
            userInput = scanner.nextLine();

            switch (userInput) {
                case "f" -> facultyOperations.startOperations();
                case "g" -> generalOperations.startOperations();
                case "br" -> {FileManager.saveData(); return;}
                case "dh" -> displayHelp();
                default -> {
                    System.out.println("No such command");
                }
            }
        }
    }
    private static void displayHelp() {
        System.out.println("""
                            f - Go to Faculty Operations
                            g - Go to General Operations
                                                    
                            dh - Display Help                        
                            br - Exit and Save Program
                            """);
    }
}
