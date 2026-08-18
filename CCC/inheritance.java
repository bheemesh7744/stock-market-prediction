interface  Addition{
    // void add(){
    //     int a=10,b=20;
    //     System.out.println("add: "+(a+b));
    //      }
    }
class Subt{
    void sub(){
            int a=1,b=5;
            System.out.println("sub: "+(a-b));
        }
    }
class Mult extends Subt implements Addition{
    void mul(){
        int a=1,b=6;
        System.out.println("mul: "+(a*b));
    }
    void add(){
        int a=1,b=2;
        System.out.println("add: "+(a+b));
     }
}
public class inheritance {
    public static void main(String[] args) {
        Mult s= new Mult();
        s.sub();
        s.add();
        s.mul();
        

    }
}