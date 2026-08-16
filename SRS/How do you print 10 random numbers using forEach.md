<!--
reps: 0
priority: 0
-->
#Java/Streams #Career/Interview/Exercises #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как вывести на экран 10 случайных чисел, используя `forEach()`?**

```java
(new Random())
    .ints()
    .limit(10)
    .forEach(System.out::println);
```
