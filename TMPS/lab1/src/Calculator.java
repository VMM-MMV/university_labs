import interfaces.shapes.Areable;
import interfaces.shapes.Lengthable;
import interfaces.shapes.Perimeterable;

public class Calculator {

    public void calculateArea(Areable shape) {
        double area = shape.getArea();
        System.out.println("Area: " + area);
    }

    public void calculatePerimeter(Perimeterable shape) {
        double perimeter = shape.getPerimeter();
        System.out.println("Perimeter: " + perimeter);
    }

    public void calculateLength(Lengthable shape) {
        double length = shape.getLength();
        System.out.println("Length: " + length);
    }
}
