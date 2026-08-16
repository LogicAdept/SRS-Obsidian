<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужны функциональные интерфейсы `Predicate<T>`, `DoublePredicate`, `IntPredicate` и `LongPredicate`?**

__`Predicate<T>` (предикат)__ - интерфейс, с помощью которого реализуется функция, получающая на вход экземпляр класса `T` и возвращающая на выходе значение типа `boolean`.

Интерфейс содержит различные методы по умолчанию, позволяющие строить сложные условия (`and`, `or`, `negate`).

```java
Predicate<String> predicate = (s) -> s.length() > 0;
predicate.test("foo"); // true
predicate.negate().test("foo"); // false
```

+ `DoublePredicate` - предикат получающий на вход `Double`;
+ `IntPredicate` - предикат получающий на вход `Integer`;
+ `LongPredicate` - предикат получающий на вход `Long`.
