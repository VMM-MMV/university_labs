import DataBase.LoadData;
import DataBase.SaveData;
import OperationLogic.FacultyOperations;
import OperationLogic.GeneralOperations;

import static OperationLogic.CommonOperationObjects.scanner;

public class MainApp {
    public static void main(String[] args) {
        new LoadData();
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
                case "br" -> {new SaveData(); return;}
                case "help" -> {
                    System.out.println("""
                            f - Go to Faculty Operations
                            g - Go to General Operations
                                                    
                            br - Exit and Save Program
                            """);
                }
                default -> {
                    System.out.println("No such command");
                }
            }
        }

    }
}
