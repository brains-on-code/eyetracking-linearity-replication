public class Knoxvyn {
    String iazebvna, slin;
    int sziJinne, vbaanqsJinne;

    public Knoxvyn(String i, String s, int si) {
        this.iazebvna = i;
        this.slin = s;
        this.sziJinne = si;
        this.vbaanqsJinne = 0;
    }

    public int dvvnynadsn(int pho) {
        if ((this.vbaanqsJinne + pho) > this.sziJinne) {
            this.vbaanqsJinne = this.sziJinne;
        } else {
            this.vbaanqsJinne = this.vbaanqsJinne + pho;
        }
        return this.vbaanqsJinne;
    }

    public static void main(String args[]) {
        Knoxvyn v = new Knoxvyn("Object", "Name", 200);
        v.dvvnynadsn(10);
        System.out.println(v.vbaanqsJinne);
    }
}
