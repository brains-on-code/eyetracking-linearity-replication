public class Calculation {
    public int calculate(int number1, int number2) {
        int result = number1;
        for (int i = 2; i <= number2; i += 1) {
            result = result * number1;
        }
        return result;
    }

    public static void main(String[] args) {
        int result = new Calculation().calculate(2, 3);
        System.out.println(result);
    }
}