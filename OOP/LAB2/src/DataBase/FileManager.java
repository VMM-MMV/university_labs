package DataBase;

import OperationLogic.Storage;
import Templates.Faculty;

import java.io.*;
import java.util.ArrayList;

public class FileManager {

    public static void saveData() {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data.ser"))) {
            out.writeObject(Storage.getAllFacultiesList());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void loadData() {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("data.ser"))) {
            Object obj1 = in.readObject();
            if (obj1 instanceof ArrayList) {
                ArrayList<Faculty> faculties =  (ArrayList<Faculty>) obj1;
                Storage.loadFaculties(faculties);
            }
        } catch (NullPointerException | IOException | ClassNotFoundException e) {
            System.out.println("Data Base is empty.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
