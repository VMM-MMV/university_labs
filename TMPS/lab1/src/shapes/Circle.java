package shapes;

import interfaces.shapes.Areable;
import interfaces.shapes.Perimeterable;

public class Circle implements Areable, Perimeterable {
    private final double radius;
    private final double PI = 3.14;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double getArea() {
        return PI * radius * radius;
    }

    @Override
    public double getPerimeter() {
        return 2 * PI * radius;
    }
}
