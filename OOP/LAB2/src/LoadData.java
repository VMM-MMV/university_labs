import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.util.ArrayList;

public class LoadData {
    LoadData() {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("data.ser"))) {
            Object obj1 = in.readObject();
            if (obj1 instanceof ArrayList) {
                Operations.studentFaculties = (ArrayList<StudentFaculty>) obj1;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
