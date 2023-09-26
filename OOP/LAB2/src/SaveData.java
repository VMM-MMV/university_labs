import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;

public class SaveData {
    SaveData() {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data.ser"))) {
            out.writeObject(Operations.studentFaculties);
            out.writeObject(Operations.graduatedFromFaculties);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
