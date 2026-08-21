<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/TryCatch #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Можно ли в catch ловить Throwable? Стоит ли?**

Можно, но не стоит — поймаешь и Error (OutOfMemoryError, StackOverflowError), которые обычно нельзя восстанавливать. Лови конкретные исключения.
