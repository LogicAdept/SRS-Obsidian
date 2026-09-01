<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/JVM #Career/Interview/Exercises #SRS #New
```java
   public class Test {  
  
     public Test() {  
       s1 = sP1("1");  
     }  
  
     static String s1 = sP1("a");  
  
     String s3 = sP1("2");  
  
     {  
       s1 = sP1("3");  
     }  
  
     static {  
       s1 = sP1("b");  
     }  
  
     static String s2 = sP1("c");  
  
     public static void main(String args[]) {  
       Test ft = new Test();  
     }  
  
     private static String sP1(String s) {  
       System.out.println(s);  
       return s;  
     }  
  
     String s4 = sP1("4");  
   }  
  
   -----  
   a b c 2 3 4 1
```
