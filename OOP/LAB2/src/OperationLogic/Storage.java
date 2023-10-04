package OperationLogic;

import Templates.Faculty;

import java.util.ArrayList;

public class Storage {
    private static ArrayList<Faculty> allFacultiesList = new ArrayList<>();

    public static ArrayList<Faculty> getAllFacultiesList() {
        return allFacultiesList;
    }

    public static void addFaculty(Faculty faculty) {
        allFacultiesList.add(faculty);
    }

    public static void loadFaculties(ArrayList<Faculty> faculties) {
        allFacultiesList = faculties;
    }
}
