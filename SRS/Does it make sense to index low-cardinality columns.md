<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по оптимизации SQL-запросов (2026). Не сверен с официальной документацией СУБД. Не считать ответом для ревью.

**Boolean index usefulness?**

Alone, rarely — seq scan wins. Partial index WHERE active AND ... or composite (low_card, high_card) after a selective equality. Bitmap AND can combine a weak index with a strong one.
