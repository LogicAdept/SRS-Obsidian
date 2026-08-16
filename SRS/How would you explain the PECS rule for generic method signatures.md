<!--
reps: 0
priority: 0
-->
#Java/Generics #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Generics: PECS. Что означает ? extends T и ? super T?**

Producer Extends, Consumer Super. extends — можно читать, нельзя писать; super — наоборот.

**Generics: type erasure, PECS.**

Type erasure: в рантайме нет типового параметра. PECS: Producer Extends (читать), Consumer Super (писать). Wildcard <?> — только чтение как Object.

**Generics: type erasure и PECS.**

Дженерики стираются компилятором (type erasure) — в рантайме нет информации о типовом параметре. PECS: Producer Extends, Consumer Super. List<? extends Number> — читать, List<? super Integer> — писать.
