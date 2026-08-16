<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие существуют способы перебирать элементы списка?**

+ Цикл с итератором

```java
Iterator<String> iterator = list.iterator();
while (iterator.hasNext()) {
    //iterator.next();
}
```

+ Цикл `for`

```java
for (int i = 0; i < list.size(); i++) {
    //list.get(i);
}
```

+ Цикл `while`

```java
int i = 0;
while (i < list.size()) {
    //list.get(i);
    i++;
}
```

+ «for-each»

```java
for (String element : list) {
    //element;
}
```
