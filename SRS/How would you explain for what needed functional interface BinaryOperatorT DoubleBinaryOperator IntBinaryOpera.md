<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужны функциональные интерфейсы `BinaryOperator<T>`, `DoubleBinaryOperator`, `IntBinaryOperator` и `LongBinaryOperator`?**

__`BinaryOperator<T>` (бинарный оператор)__ - интерфейс, с помощью которого реализуется функция, получающая на вход два экземпляра класса `T` и возвращающая на выходе экземпляр класса `T`.
```java
BinaryOperator<Integer> operator = (a, b) -> a + b;
System.out.println(operator.apply(1, 2)); // 3
```

+ `DoubleBinaryOperator` - бинарный оператор получающий на вход `Double`;
+ `IntBinaryOperator` - бинарный оператор получающий на вход `Integer`;
+ `LongBinaryOperator` - бинарный оператор получающий на вход `Long`.
