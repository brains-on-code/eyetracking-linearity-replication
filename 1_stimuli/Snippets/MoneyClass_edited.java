public class MoneyClass {
    public static void main(String[] args) {
        int cents = 140;
        int dollars = cents / 100;
        int restCents = cents % 100;
        System.out.print(dollars + "," + restCents);
    }
}
