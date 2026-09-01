<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Можно ли реализовать метод `equals()` класса `MyClass` вот так: `class MyClass {public boolean equals(MyClass that) {return this == that;}}`?**

Реализовать можно, но данный метод не переопределяет метод `equals()` класса `Object`, а перегружает его.
