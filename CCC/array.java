import java.util.*;

public class array {
     public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        int n=sc.nextInt();
        int[] a=new int[n];
        for(int i=0;i<n;i++){
            a[i]=sc.nextInt();
        }
        System.out.println("enter key : ");
        int key=sc.nextInt();
        int f=0;
        for(int i=0;i<n;i++){
            if(a[i]==key){
                f=1;
                System.out.println("element found at index "+(i+1));
                break;
            }
        }
        if(f==0){
            System.out.println("element not found");
        }
    }
    
     }
