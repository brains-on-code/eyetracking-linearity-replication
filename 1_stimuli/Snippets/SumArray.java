public class SumArray {
    public static void main(String[] args) {
        int[] array = { 1, 6, 4, 10, 2 };

        int result = 0;
        for (int i = 0; i <= array.length - 1; i++) {
            result = result + array[i];
        }

        System.out.println(result);
    }
}
