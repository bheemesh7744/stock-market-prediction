
import java.util.Scanner;

public class largest {
    public static void main(String[] args) {
        Scanner Sc=new Scanner(System.in);
        System.out.println("enter a number");
        int n1=Sc.nextInt();
         System.out.println("enter a number");
        int n2=Sc.nextInt();
         System.out.println("enter a number");
        int n3=Sc.nextInt();
        if(n1>=n2 && n1>=n3){
            System.out.println(" the largest is:"+n1);
        }
        else if(n2>=n1 && n2>=n3){
            System.out.println("the  largest is: "+n2);
        }
        else{
            System.out.println("the  largest is: "+n3);
        }
    }
    
}
