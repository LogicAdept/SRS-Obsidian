<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/SynchronizedKeyword #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**На каком объекте происходит синхронизация при вызове `static synchronized` метода?**

У синхронизированного статического метода нет доступа к `this`, но есть доступ к объекту класса `Class`, он присутствует в единственном экземпляре и именно он выступает в качестве монитора для синхронизации статических методов. Таким образом, следующая конструкция:

```java
public class SomeClass {

    public static synchronized void someMethod() {
        //code
    }
}
```

эквивалентна такой:

```java
public class SomeClass {

    public static void someMethod(){
        synchronized(SomeClass.class){
            //code
        }
    }
}
```
