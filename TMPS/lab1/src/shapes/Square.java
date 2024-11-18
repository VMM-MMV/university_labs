package shapes;

import interfaces.shapes.Areable;
import interfaces.shapes.Lengthable;
import interfaces.shapes.Perimeterable;

public class Square implements Areable, Perimeterable, Lengthable {
    private final double length;

    public Square(double length) {
        this.length = length;
    }

    @Override
    public double getArea() {
        return length * length;
    }

    @Override
    public double getPerimeter() {
        return 4 * length;
    }

    @Override
    public double getLength() {
        return length;
    }
}
