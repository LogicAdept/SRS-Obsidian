<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как вывести на экран количество пустых строк с помощью метода `filter()`?**

```java
System.out.println(
    Stream
        .of("Hello", "", ", ", "world", "!")
        .filter(String::isEmpty)
        .count());
```
