import DataBase.LoadData;
import OperationLogic.FacultyOperations;
import OperationLogic.GeneralOperations;

import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

import static OperationLogic.CommonOperationObjects.allFacultiesList;
import static OperationLogic.CommonOperationObjects.scanner;

public class MainApp {
    public static void main(String[] args) {
        new LoadData();
        mainMenu();
    }

    public static void mainMenu() {
        FacultyOperations facultyOperations = new FacultyOperations();
        String userInput;
        while(true) {

            System.out.println("Enter something:");
            userInput = scanner.nextLine();

            switch (userInput) {
                case "f" -> facultyOperations.startOperations();
                case "g" -> GeneralOperations.startOperations();
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

    public static class SaveData {
        SaveData() {
            try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data.ser"))) {
                out.writeObject(allFacultiesList);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
