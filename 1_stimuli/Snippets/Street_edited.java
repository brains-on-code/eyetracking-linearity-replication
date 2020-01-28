public class Street {
    private int number;

    public Street(int nr) {
        setNumber(nr);
    }

    public int getNumber() {
        return number;
    }

    public void setNumber(int number) {
        this.number = number;
    }

    public static void main(String[] args) {
        Street street = new Street(5);
        street.setNumber(15);
        System.out.print(street.getNumber());
    }
}
