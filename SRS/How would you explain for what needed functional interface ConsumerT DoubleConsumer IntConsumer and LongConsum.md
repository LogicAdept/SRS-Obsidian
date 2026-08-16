<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужны функциональные интерфейсы `Consumer<T>`, `DoubleConsumer`, `IntConsumer` и `LongConsumer`?**

__`Consumer<T>` (потребитель)__ - интерфейс, с помощью которого реализуется функция, которая получает на вход экземпляр класса `T`, производит с ним некоторое действие и ничего не возвращает.

```java
Consumer<String> hello = (name) -> System.out.println("Hello, " + name);
hello.accept("world");
```

+ `DoubleConsumer` - потребитель получающий на вход `Double`;
+ `IntConsumer` - потребитель получающий на вход `Integer`;
+ `LongConsumer` - потребитель получающий на вход `Long`.
