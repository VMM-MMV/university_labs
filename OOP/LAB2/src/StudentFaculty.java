import java.util.List;

public class StudentFaculty extends Faculty{
    public StudentFaculty(String name, String abbreviation, List<Student> students, StudyField studyField) {
        super(name, abbreviation, students, studyField);
    }
}
