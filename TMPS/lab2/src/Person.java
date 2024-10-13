package src;

public class Person implements Prototype, PoolObject {
    private String firstName; // Required
    private String lastName;  // Required
    private int age;          // Optional
    private String address;   // Optional
    private String phone;     // Optional

    public Person() {}

    private Person(Builder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.age = builder.age;
        this.address = builder.address;
        this.phone = builder.phone;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public int getAge() {
        return age;
    }

    public String getAddress() {
        return address;
    }

    public String getPhone() {
        return phone;
    }

    @Override
    public String toString() {
        return "Person{" +
                "firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", age=" + age +
                ", address='" + address + '\'' +
                ", phone='" + phone + '\'' +
                '}';
    }

    @Override
    public Person clone() {
        return new Builder(this.firstName, this.lastName)
                        .age(this.age)
                        .address(this.address)
                        .phone(this.phone).build();
    }

    @Override
    public void reset() {
        this.firstName = null;
        this.lastName = null;
        this.age = 0;
        this.address = null;
        this.phone = null;
    }

    public static class Builder {
        private final String firstName;
        private final String lastName;
        private int age;
        private String address;
        private String phone;

        public Builder(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public Builder age(int age) {
            this.age = age;
            return this;
        }

        public Builder address(String address) {
            this.address = address;
            return this;
        }

        public Builder phone(String phone) {
            this.phone = phone;
            return this;
        }

        public Person build() {
            return new Person(this);
        }
    }
}