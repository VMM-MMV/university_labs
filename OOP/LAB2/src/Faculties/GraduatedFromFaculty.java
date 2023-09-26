package Faculties;

import Templates.Student;
import Templates.StudyField;
import java.util.List;

public class GraduatedFromFaculty extends Faculty {
    public GraduatedFromFaculty(String name, String abbreviation, List<Student> students, StudyField studyField) {
        super(name, abbreviation, students, studyField);
    }
}
