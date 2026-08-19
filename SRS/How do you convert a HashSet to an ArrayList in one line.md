<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Set/HashSet #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как одной строчкой преобразовать `HashSet` в `ArrayList`?**

```java
ArrayList<Integer> list = new ArrayList<>(new HashSet<>());
```

**Как одной строчкой преобразовать `ArrayList` в `HashSet`?**

```java
HashSet<Integer> set = new HashSet<>(new ArrayList<>());
```
