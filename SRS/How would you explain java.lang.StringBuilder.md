<!--
reps: 0
priority: 0
-->
#Java/String #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**String vs StringBuilder vs StringBuffer.**

String: immutable, при конкатенации создаёт новый объект. StringBuilder: mutable, НЕ потокобезопасный (быстрый). StringBuffer: mutable, потокобезопасный (synchronized — медленнее). В цикле конкатенация String → O(n²), StringBuilder → O(n). Компилятор оптимизирует простые случаи, но не циклы.
