<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужны функциональные интерфейсы `Supplier<T>`,  `BooleanSupplier`, `DoubleSupplier`, `IntSupplier` и `LongSupplier`?**

__`Supplier<T>` (поставщик)__ - интерфейс, с помощью которого реализуется функция, ничего не принимающая на вход, но возвращающая на выход результат класса `T`;

```java
Supplier<LocalDateTime> now = LocalDateTime::now;
now.get();
```

+ `DoubleSupplier` - поставщик возвращающий `Double`;
+ `IntSupplier` - поставщик возвращающий `Integer`;
+ `LongSupplier` - поставщик возвращающий `Long`.
