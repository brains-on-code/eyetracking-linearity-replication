public class Warwmrabkyn {
    public int warwmrabs(int nmclsf1, int nmclsf2) {
        int fsqmrb = nmclsf1;
        for (int i = 2; i <= nmclsf2; i += 1) {
            fsqmrb = fsqmrb * nmclsf1;
        }
        return fsqmrb;
    }

    public static void main(String[] args) {
        int fsqmrb = new Warwmrabkyn().warwmrabs(2, 3);
        System.out.println(fsqmrb);
    }
}
