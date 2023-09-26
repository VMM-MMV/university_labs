package DataBase;

import Templates.Faculty;
import OperationLogic.Storage;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.ArrayList;

public class LoadData {
    public LoadData() {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("data.ser"))) {
            Object obj1 = in.readObject();
            if (obj1 instanceof ArrayList) {
                Storage.allFacultiesList = (ArrayList<Faculty>) obj1;
            }
        } catch (NullPointerException | IOException | ClassNotFoundException e) {
            System.out.println("Data Base is empty.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
