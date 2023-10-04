package OperationLogic;

import DataBase.FileManager;
import Logging.Logger;
import Templates.Faculty;
import Templates.Student;
import Templates.StudyField;

import java.util.ArrayList;
import java.util.Objects;

import static OperationLogic.UserInput.scanner;

public class GeneralOperations {
    static Logger logger = new Logger();
    public void startOperations() {
        String result;
        String userInput;

        do {
            System.out.println("G: Enter command:");

            userInput = scanner.nextLine();
            result = doOperations(userInput);
        } while (!result.equals("bk"));
    }

    private String doOperations(String userInput) {
        if (userInput.length() < 2) {
            System.out.println("String is too short!");
            return "";
        }

        String commandCall = userInput.substring(0, 2);
        String commandOperation = userInput.substring(2);


        switch (Objects.requireNonNull(commandCall)) {
            case "nf" -> newFaculty(commandOperation);
            case "ss" -> searchStudent(commandOperation);
            case "df" -> displayFaculties(commandOperation);
            case "br" -> { FileManager.saveData(); System.exit(0); }
            case "bk" -> { return "bk"; }
            case "dh" -> displayHelp();
            default -> System.out.println("No such command");
        }
        return "";
    }

    private void newFaculty(String commandOperation) {
        var parts = commandOperation.split("/");

        if (parts.length < 4) {
            System.out.println("Incomplete command operation.");
            return;
        }

        String facultyName = parts[1];
        String facultyAbbreviation = parts[2];
        StudyField studyField = StudyField.valueOf(parts[3]);

        Storage.addFaculty(new Faculty(facultyName, facultyAbbreviation, new ArrayList<>(), studyField));
        logger.log("Created faculty " + facultyAbbreviation);
    }

    private void searchStudent(String commandOperation) {
        var parts = commandOperation.split("/");
        if (parts.length < 2) {
            System.out.println("Incomplete command operation.");
            return;
        }

        String studentEmail = parts[1];

        for (Faculty faculty : Storage.getAllFacultiesList()) {
            for (Student student : faculty.getStudents()) {
                if (Objects.equals(student.getEmail(), studentEmail)) {
                    System.out.println("Student is present in faculty: " + faculty.getName());
                    return;
                }
            }
        }

        System.out.println("Student is not present in any faculty");
    }

    private static void displayFaculties() {
        for (Faculty faculty: Storage.getAllFacultiesList()) {
                System.out.println("Name: " + faculty.getName() + " | Abbreviation: " + faculty.getAbbreviation() + " | Field: " + faculty.getStudyField());
        }
    }

    private void displayFaculties(String commandOperation) {
        var parts = commandOperation.split("/");

        if (parts.length < 2) {
            displayFaculties();
            return;
        }

        StudyField studyField;
        try {
            studyField = StudyField.valueOf(parts[1]);
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid studyField");
            return;
        }


        for (Faculty faculty: Storage.getAllFacultiesList()) {
            if (faculty.getStudyField() == studyField) {
                System.out.println("Name: " + faculty.getName() + " | Abbreviation: " + faculty.getAbbreviation() + " | Field: " + faculty.getStudyField());
            }
        }
    }
    private void displayHelp() {
        System.out.println("""
                General operations
                
                nf/<faculty name>/<faculty abbreviation>/<field> - create (n)ew (f)aculty
                ss/<student email> - (s)earch (s)tudent and show faculty
                df - (d)isplay all (f)aculties
                df/<field> - (d)isplay all faculties of a (f)ield

                bk - back
                br - exit and save
                dh - (d)isplay (h)elp""");
    }
}
