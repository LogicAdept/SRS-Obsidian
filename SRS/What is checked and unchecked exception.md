<!--
reps: 0
priority: 0
-->
#Java/Language #Java/Exceptions/Checked #Java/Exceptions/Unchecked #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое _checked_ и _unchecked exception_?**

В Java все исключения делятся на два типа:

+ __checked (контролируемые/проверяемые исключения)__ должны обрабатываться блоком `catch` или описываться в сигнатуре метода (например `throws IOException`). Наличие такого обработчика/модификатора сигнатуры проверяются на этапе компиляции;
+ __unchecked (неконтролируемые/непроверяемые исключения)__, к которым относятся ошибки `Error` (например `OutOfMemoryError`), обрабатывать которые не рекомендуется и исключения времени выполнения, представленные классом `RuntimeException` и его наследниками (например `NullPointerException`), которые могут не обрабатываться блоком `catch` и не быть описанными в сигнатуре метода.

**Какие существуют _unchecked exception_?**

Наиболее часто встречающиеся: `ArithmeticException`, `ClassCastException`, `ConcurrentModificationException`, `IllegalArgumentException`, `IllegalStateException`, `IndexOutOfBoundsException`, `NoSuchElementException`, `NullPointerException`, `UnsupportedOperationException`.
