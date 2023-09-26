package Faculties;

import java.io.Serializable;
import java.util.List;
import java.util.Objects;
import Templates.Student;
import Templates.StudyField;


public abstract class Faculty implements Serializable {
    private final String name;
    private final String abbreviation;
    private final List<Student> students;
    private final StudyField studyField;

    Faculty(String name, String abbreviation, List<Student> students, StudyField studyField) {
        this.name = Objects.requireNonNull(name, "name must not be null");
        this.abbreviation = Objects.requireNonNull(abbreviation, "abbreviation must not be null");
        this.students = Objects.requireNonNull(students, "students must not be null");
        this.studyField = Objects.requireNonNull(studyField, "studyField must not be null");
    }

    // Getter methods
    public String getName() {
        return name;
    }

    public String getAbbreviation() {
        return abbreviation;
    }

    public List<Student> getStudents() {
        return students;
    }

    public StudyField getStudyField() {
        return studyField;
    }

    public void addStudent(Student student) {
        this.students.add(student);
    }

    public void removeStudent(Student student) {
        this.students.remove(student);
    }

}
