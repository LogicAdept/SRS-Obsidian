#Career/Interview/Exercises #Java/Lambdas #SRS #New
<!--
reps: 0
priority: 0
-->
```java
static class Person {  
        int age;  
    }  
  
    public static void main(String args[]) {  
        Person p = new Person();
        Supplier<Person> se = () -> { p.age = 40; return p; }; // 1  
        p.age = 50; // 2  
        System.out.println(se.get().age); // 3  
    }  
  
    -----  
    40
```