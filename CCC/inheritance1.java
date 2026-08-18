class animal{
    void eat(){
        System.out.println(" i eat anything");
    }
}
class dog extends animal{
    void drink(){
        System.out.println("drink only water");
    }
    void horse(){
        System.out.println("i am dog");
    }
}
public class inheritance1 {
    public static void main(String[] args){
         dog d=new dog();
         d.horse();
         d.eat();
         d.drink();
    }
    
}
