public class Boihcpujo {
    private int t1, w1, t2, w2;

    public Boihcpujo(int t1, int w1, int t2, int w2) {
        this.t1 = t1;
        this.w1 = w1;
        this.t2 = t2;
        this.w2 = w2;
    }

    public int qalhx() {
        return this.t2 - this.t1;
    }

    public int xoauxh() {
        return this.w2 - this.w1;
    }

    public double cboc() {
        return this.qalhx() * this.xoauxh();
    }

    public static void main(String[] args) {
        Boihcpujo boih1 = new Boihcpujo(0, 0, 10, 10);
        System.out.print(boih1.cboc());
        Boihcpujo boih2 = new Boihcpujo(5, 5, 10, 10);
        System.out.print("" + boih2.cboc());
    }
}


