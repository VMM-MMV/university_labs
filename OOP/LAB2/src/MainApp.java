import DataBase.FileManager;
import OperationLogic.FacultyOperations;
import OperationLogic.GeneralOperations;
import OperationLogic.Scanner;


public class MainApp {
    public static void main(String[] args) {
        FileManager.loadData();
        mainMenu();
    }

    public static void mainMenu() {
        FacultyOperations facultyOperations = new FacultyOperations();
        GeneralOperations generalOperations = new GeneralOperations();
        String userInput;
        while(true) {

            System.out.println("Enter something:");
            userInput = Scanner.getCommandScanner().nextLine();

            switch (userInput) {
                case "f" -> facultyOperations.startOperations();
                case "g" -> generalOperations.startOperations();
                case "br" -> {FileManager.saveData(); return;}
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
