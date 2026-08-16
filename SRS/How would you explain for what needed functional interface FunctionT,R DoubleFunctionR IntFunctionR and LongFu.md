<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужны функциональные интерфейсы `Function<T,R>`, `DoubleFunction<R>`, `IntFunction<R>` и `LongFunction<R>`?**

__`Function<T, R>`__ - интерфейс, с помощью которого реализуется функция, получающая на вход экземпляр класса `T` и возвращающая на выходе экземпляр класса `R`.

Методы по умолчанию могут использоваться для построения цепочек вызовов (`compose`, `andThen`).

```java
Function<String, Integer> toInteger = Integer::valueOf;
Function<String, String> backToString = toInteger.andThen(String::valueOf);
backToString.apply("123");     // "123"
```

+ `DoubleFunction<R>` - функция получающая на вход `Double` и возвращающая на выходе экземпляр класса `R`;
+ `IntFunction<R>` - функция получающая на вход `Integer` и возвращающая на выходе экземпляр класса `R`;
+ `LongFunction<R>` - функция получающая на вход `Long` и возвращающая на выходе экземпляр класса `R`.
