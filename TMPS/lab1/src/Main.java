import shapes.Circle;
import shapes.Line;
import shapes.Square;

public class Main {
    public static void main(String[] args) {
        Circle circle = new Circle(5);
        Square square = new Square(4);
        Line line = new Line(10);

        Calculator calculator = new Calculator();

        calculator.calculateArea(circle);
        calculator.calculateArea(square);

        calculator.calculatePerimeter(circle);
        calculator.calculatePerimeter(square);

        calculator.calculateLength(line);
        calculator.calculateLength(square);
    }
}
