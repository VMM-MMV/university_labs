import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Objects;
import java.util.Scanner;

public class GeneralOperations extends Operations{
    static void startOperations() {
        Scanner scanner = new Scanner(System.in);
        String result;

        do {
            System.out.println("G: Enter command:");
            String userInput = scanner.nextLine();

            result = checkInput(userInput);
        } while (!result.equals("bk") && !result.equals("br"));

        if (result.equals("br")) { return; }

        MainApp.mainMenu();
    }

    private static @NotNull String checkInput(@NotNull String userInput) {
        if (userInput.length() < 2) {
            System.out.println("String is too short!");
            return "";
        }

        String commandCall = userInput.substring(0, 2);
        String commandOperation = userInput.substring(2);


        switch (Objects.requireNonNull(commandCall)) {
            case "nf" -> newFaculty(commandOperation);
            case "ss" -> searchStudent();
            case "df" -> displayFaculties();
            case "br" -> { return "br"; }
            case "bk" -> { return "bk"; }
            default -> System.out.println("No such command");
        }
        return "";
    }

    private static void newFaculty(@NotNull String commandOperation) {
        String[] parts = commandOperation.split("/");
        String facultyName = parts[1];
        String facultyAbbreviation = parts[2];
        StudyField studyField = StudyField.valueOf(parts[3]);

        studentFaculties.add(new StudentFaculty(facultyName, facultyAbbreviation, new ArrayList<>(), studyField));
    }
    // nf/fcimbig/fcim/URBANISM_ARCHITECTURE

    private static void searchStudent() {
        System.out.println("searchStudent");
    }

    private static void displayFaculties() {
        for (StudentFaculty studentFaculty: studentFaculties) {
            System.out.println("Name: " + studentFaculty.getName() + " | Abbreviation: " + studentFaculty.getAbbreviation() + " | Field: " + studentFaculty.getStudyField());
        }
    }
}
