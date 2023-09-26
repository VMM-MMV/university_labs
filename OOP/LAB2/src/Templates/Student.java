package Templates;

import OperationLogic.StudentRole;

import java.io.Serializable;
import java.util.Date;
import java.util.Objects;

public class Student implements Serializable {
    private String firstName;
    private String lastName;
    private String email;
    private Date enrollmentDate;
    private Date dateOfBirth;
    private StudentRole studentRole;

    public Student(String firstName, String lastName, String email, Date enrollmentDate, Date dateOfBirth, StudentRole studentRole) {
        this.firstName = Objects.requireNonNull(firstName, "firstName must not be null");
        this.lastName = Objects.requireNonNull(lastName, "lastName must not be null");
        this.email = Objects.requireNonNull(email, "email must not be null");
        this.enrollmentDate = Objects.requireNonNull(enrollmentDate, "enrollmentDate must not be null");
        this.dateOfBirth = Objects.requireNonNull(dateOfBirth, "dateFormat must not be null");
        this.studentRole = Objects.requireNonNull(studentRole, "studentRole must not be null");
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public Date getDateOfBirth() {
        return dateOfBirth;
    }

    public Date getEnrollmentDate() {
        return enrollmentDate;
    }
    public void setStudentRole(StudentRole role) {
        this.studentRole = role;
    }
    public StudentRole getStudentRole() {
        return studentRole;
    }
}
