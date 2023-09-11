public class Human {
    //We set variables that a normal human should have
    public String name;
    public int age;
    public String favoriteAnime;
    public String burried = "In the ground";

    public void live() {
        System.out.println("He be livin'");
    }
    public void laugh() {
        System.out.println("Ha Ha");
    }

    public void cry() {
        System.out.println("Sniff Sniff");
    }

    public String burriedWhere() {
        return burried;
    }
}
