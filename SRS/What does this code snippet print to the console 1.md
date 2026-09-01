<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Collections/List/Vector #Java/Language/Parameters #SRS #New
```java
    public static void main(String args[]) {  
        Stack s1 = new Stack();  
        Stack s2 = new Stack();  
        processStacks(s1, s2);  
        System.out.println(s1 + " " + s2);  
    }  
  
    public static void processStacks(Stack x1, Stack x2) {  
        x1.push(new Integer ("100"));  
        x2 = x1;  
    }  
  
    // [] [], [100] [100], [100] [], [] [100]  
  
    -----  
    [100] []
```