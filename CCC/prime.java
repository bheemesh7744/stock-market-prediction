import java.util.*;
public class prime {
    public static void main(String[] args) {
        Scanner Sc=new Scanner(System.in);
        System.out.println("enter a number");
        int n=Sc.nextInt();
        if(n<=1){
            System.out.println(" not prime");
            return;
        }
        boolean isPrime = true;
        for(int i=2;i<=n-1;i++){
            if(n%i==0){
                isPrime=false;
                break;
            }
        }
        if(isPrime){
            System.out.println("prime");
        }
        else{
            System.out.println("not prime");
        }
        
    }
}
