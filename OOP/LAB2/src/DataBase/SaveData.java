package DataBase;

import OperationLogic.Storage;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;

public class SaveData {
    public static void main(String[] args) {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data.ser"))) {
            out.writeObject(Storage.allFacultiesList);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

