<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Каким образом реализованы методы `hashCode()` и `equals()` в классе `Object`?**

Реализация метода `Object.equals()` сводится к проверке на равенство двух ссылок:

```java
public boolean equals(Object obj) {
  return (this == obj);
}
```

Реализация метода `Object.hashCode()` описана как `native`, т.е. определенной не с помощью Java кода и обычно возвращает адрес объекта в памяти:

```java
public native int hashCode();
```
