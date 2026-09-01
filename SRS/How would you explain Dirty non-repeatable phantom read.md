<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Dirty / non-repeatable / phantom read.**

Dirty — чтение незакоммиченных данных. Non-repeatable — два чтения одной строки дают разный результат. Phantom — два SELECT с WHERE возвращают разное число строк.
