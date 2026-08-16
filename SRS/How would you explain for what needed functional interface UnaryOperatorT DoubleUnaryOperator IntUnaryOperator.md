<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужны функциональные интерфейсы `UnaryOperator<T>`, `DoubleUnaryOperator`, `IntUnaryOperator` и `LongUnaryOperator`?**

__`UnaryOperator<T>` (унарный оператор)__ принимает в качестве параметра объект типа `T`, выполняет над ними операции и возвращает результат операций в виде объекта типа `T`:

```java
UnaryOperator<Integer> operator = x -> x * x;
System.out.println(operator.apply(5)); // 25
```

+ `DoubleUnaryOperator` - унарный оператор получающий на вход `Double`;
+ `IntUnaryOperator` - унарный оператор получающий на вход `Integer`;
+ `LongUnaryOperator` - унарный оператор получающий на вход `Long`.
