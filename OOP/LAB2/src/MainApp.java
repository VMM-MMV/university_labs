import DataBase.LoadData;
import OperationLogic.FacultyOperations;
import OperationLogic.Storage;
import OperationLogic.GeneralOperations;

import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.util.Scanner;

public class MainApp {
    public static void main(String[] args) {
        new LoadData();
        mainMenu();
    }

    public static void mainMenu() {
        Scanner scanner;
        String userInput;
        while(true) {
            scanner = new Scanner(System.in);

            System.out.println("Enter something:");
            userInput = scanner.nextLine();

            switch (userInput) {
                case "f" -> FacultyOperations.startOperations();
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
                out.writeObject(Storage.allFacultiesList);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
