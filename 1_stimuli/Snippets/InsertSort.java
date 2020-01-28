public class InsertSort {
    public static int[] sort(int[] unsorted) {
        for (int i = 1; i < unsorted.length; i++) {
            sort(i, unsorted);
        }
        return unsorted;
    }

    private static void sort(int i, int[] unsorted) {
        for (int j = i; j > 0; j--) {
            int jthElement = unsorted[j];
            int jMinusOneElement = unsorted[j - 1];
            if (jthElement > jMinusOneElement) {
                unsorted[j - 1] = jthElement;
                unsorted[j] = jMinusOneElement;
            } else {
                break;
            }
        }
    }

    public static void main(String[] args) {
        int[] unsorted = { 3, 7, 4, 5 };
        int[] result = sort(unsorted);
        for (int i = 0; i < result.length; i++) {
          System.out.print(result[i]);
        }
    }
}
