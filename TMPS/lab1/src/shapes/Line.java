package shapes;

import interfaces.shapes.Lengthable;

public class Line implements Lengthable {
    private final double length;

    public Line(double length) {
        this.length = length;
    }

    @Override
    public double getLength() {
        return length;
    }
}
