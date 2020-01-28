public class XnlsHmjhpjw {
    private int szrgjw;

    public XnlsHmjhpjw(int hzwwjsySzrgjw) {
        szrgjw = hzwwjsySzrgjw;
    }

    public String hmjhp() {
        String ymjXnls = "";
        if (szrgjw < 0) {
            ymjXnls = "negative";
        } else if (szrgjw > 0) {
            ymjXnls = "positive";
        } else {
            ymjXnls = "null";
        }
        return ymjXnls;
    }

    public static void main(String[] args) {
        XnlsHmjhpjw szrgjw1 = new XnlsHmjhpjw(10);
        System.out.print(szrgjw1.check());
        XnlsHmjhpjw szrgjw2 = new XnlsHmjhpjw(0);
        System.out.print(" " + szrgjw2.check());
    }
}
