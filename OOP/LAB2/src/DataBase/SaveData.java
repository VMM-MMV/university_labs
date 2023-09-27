package DataBase;

import OperationLogic.CommonOperationObjects;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

public class SaveData {
    public SaveData() {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data.ser"))) {
            out.writeObject(CommonOperationObjects.allFacultiesList);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

