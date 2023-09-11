import java.util.Objects;

public class Main {
    public static void main(String[] args) {
        Peasant peasant = new Peasant();
        King king = new King();
        if(Objects.equals(peasant.burriedWhere(), king.burriedWhere())){
            System.out.println("Then who cares.");
        }
    }
}