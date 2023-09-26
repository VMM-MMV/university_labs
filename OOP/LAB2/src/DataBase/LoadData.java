package DataBase;

import Faculties.GraduatedFromFaculty;
import OperationLogic.Storage;
import Faculties.StudentFaculty;

import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.util.ArrayList;

public class LoadData {
    public LoadData() {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("data.ser"))) {
            Object obj1 = in.readObject();
            if (obj1 instanceof ArrayList) {
                Storage.studentFaculties = (ArrayList<StudentFaculty>) obj1;
            }

            Object obj2 = in.readObject();
            if (obj2 instanceof ArrayList) {
                Storage.graduatedFromFaculties = (ArrayList<GraduatedFromFaculty>) obj2;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
