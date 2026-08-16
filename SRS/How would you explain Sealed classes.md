<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Sealed classes — зачем?**

Ограничение иерархии наследования. Хорошо работает с pattern matching.

**Sealed Classes (Java 17+).**

Ограничение иерархии наследования: sealed class Shape permits Circle, Square. Компилятор гарантирует exhaustive switch. Связка с Pattern Matching for switch (Java 21).
