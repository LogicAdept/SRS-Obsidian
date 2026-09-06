<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Patterns/GoF #Java/StringBuffer #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём отличие String, StringBuilder, StringBuffer?**

String — immutable. Каждая конкатенация создаёт новый объект, в цикле это O(n²) по памяти. StringBuilder — mutable, не потокобезопасный, быстрый. StringBuffer — mutable + synchronized методы, потокобезопасный, но медленнее. В одном потоке всегда нужен StringBuilder.
