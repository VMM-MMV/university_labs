package OperationLogic;

public enum StudentRole {
    NOT_GRADUATED(1),
    GRADUATED(2);

    private final int value;

    StudentRole(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}
