<!--
reps: 0
priority: 0
-->
#Java/Collections #Java/Exceptions/Unchecked #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Приведите пример, когда какая-либо коллекция выбрасывает `UnsupportedOperationException`.**

```java
public static void main(String[] args) {
    List<Integer> list = Collections.emptyList();
    list.add(0);
}
```
