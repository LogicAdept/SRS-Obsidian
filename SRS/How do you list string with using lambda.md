<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как отсортировать список строк с помощью лямбда-выражения?**

```java
public static List<String> sort(List<String> list){
    Collections.sort(list, (a, b) -> a.compareTo(b));
    return list;
}
```
