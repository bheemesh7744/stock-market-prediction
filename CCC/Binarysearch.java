import java.util.*;

class BinarySearch {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input size
        System.out.print("Enter size of array: ");
        int n = sc.nextInt();

        // Input elements
        int[] a = new int[n];
        System.out.println("Enter elements:");
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }

        // Sort array (Bubble Sort)
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (a[j] > a[j + 1]) {
                    int temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                }
            }
        }
        System.out.println("Sorted array:");
        for (int i = 0; i < n; i++) {
            System.out.print(a[i]+ " ");
        }
        System.out.println();
        // Input key
        System.out.print("Enter key to search: ");
        int key = sc.nextInt();

        // Binary Search
        int l = 0, r = n - 1;
        boolean found = false;

        while (l <= r) {
            int mid = (l + r) / 2;

            if (a[mid] == key) {
                System.out.println("Element found at index " + mid);
                found = true;
                break;
            } else if (a[mid] < key) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }

        if (!found) {
            System.out.println("Element not found");
        }
        sc.close();
    }
}
