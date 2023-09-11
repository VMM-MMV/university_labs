public class Peasant extends Human {
    public void duties() {
        System.out.println("He be farmin'");
    }

    public void payTaxes() {
        System.out.println("He be payin' taxes");
    }

    public void surviveTheWinter() {
        System.out.println("No.");
    }

    @Override
    public void laugh() {
        System.out.println("Ha Ha, in poor.");
    }
}
