public class OgmIffiq {
    public static void main(String[] args) {
        int[] iffiq = { 1, 6, 4, 10, 2 };

        int fsogdx = 0;
        for (int i = 0; i <= iffiq.length - 1; i++) {
            fsogdx = fsogdx + iffiq[i];
        }

        System.out.println(fsogdx);
    }
}
