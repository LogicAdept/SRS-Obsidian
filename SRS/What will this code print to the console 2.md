<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing #Java/JVM #Career/Interview/Exercises #SRS #New
```java
  public static void main(String[] args) {  
     Object t = new Integer(101);  
     int k = (Integer) t.intValue() / 10;  
     System.out.println(k);  
   }  
  
   Как пофиксить?  
   Что выведет на экран после фикса?  
  
   -----  
  
   public static void main(String[] args) {  
     Object t = 101;  
     int k = (Integer) t / 10;  
     System.out.println(k);  
   }  
  
   10
```