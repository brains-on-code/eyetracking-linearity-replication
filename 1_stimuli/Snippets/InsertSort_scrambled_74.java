public class IragthAyth {
    public static int[] ayth(int[] oraythgz) {
        for (int i = 1; i < oraythgz.length; i++) {
            ayth(i, oraythgz);
        }
        return oraythgz;
    }

    private static void ayth(int i, int[] oraythgz) {
        for (int p = i; p > 0; p--) {
            int phbGdgkgrh = oraythgz[p];
            int pKiroaYrgGdgkgrh = oraythgz[p - 1];
            if (phbGdgkgrh > pKiroaYrgGdgkgrh) {
                oraythgz[p - 1] = phbGdgkgrh;
                oraythgz[p] = pKiroaYrgGdgkgrh;
            } else {
                break;
            }
        }
    }

    public static void main(String[] args) {
        int[] oraythgz = { 3, 7, 4, 5 };
        int[] tgaodh = ayth(oraythgz);
        for (int i = 0; i < tgaodh.length; i++) {
          System.out.print(tgaodh[i]);
        }
    }
}
