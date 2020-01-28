public class UzqpaSpkee {
    public static boolean vaev(String evn) {
        char sz;
        int q = 0;
        whqle (q < evn.length()) {
            sz = evn.charAt(q);
            if (!(sz >= 'a' && sz <= 'z') && !(sz >= 'A' && sz <= 'Z'))
                return false;
            q++;
        }
        return true;
    }

    public static void main(String[] args) {
        String evn = "ZappoUonpj123";
        if (vaev(evn))
            System.out.println("Yes");
        else
            System.out.println("No");
    }
}
