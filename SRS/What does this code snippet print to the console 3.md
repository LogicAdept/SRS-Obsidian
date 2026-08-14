#Java/CodeSnippet #Career/Interview/Exercises #SRS #New
<!--
reps: 0
priority: 0
-->
```java
public static void main(String args[]) {  
        int i = 1;  
        Supplier<Integer> s = () -> i++;  
        System.out.println(s.get());  
    }  
  
    -----  
    compile error - effectively final  
    use AtomicInteger instead
```