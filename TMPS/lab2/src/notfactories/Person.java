package src.notfactories;

import src.notfactories.interfaces.PoolObject;
import src.notfactories.interfaces.Prototype;

public class Person implements Prototype<Person>, PoolObject {
    private String firstName;
    private String lastName;
    private int age;
    private String address;
    private String phone;

    public Person() {}

    public Person(String firstName, String lastName, int age, String address, String phone) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.address = address;
        this.phone = phone;
    }

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
    public Person copy() {
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