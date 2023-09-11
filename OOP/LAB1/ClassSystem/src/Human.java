public abstract class Human {
    // Encapsulated instance variables
    private String name;
    private int age;
    private String favoriteAnime;
    private final String buried = "In the ground";

    // Public methods
    public void live() {
        System.out.println("He be livin'");
    }

    public void laugh() {
        System.out.println("Ha Ha");
    }

    public void cry() {
        System.out.println("Sniff Sniff");
    }

    public String getBurialPlace() {
        return buried;
    }

    // Getter and Setter methods for instance variables
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getFavoriteAnime() {
        return favoriteAnime;
    }

    public void setFavoriteAnime(String favoriteAnime) {
        this.favoriteAnime = favoriteAnime;
    }
}
