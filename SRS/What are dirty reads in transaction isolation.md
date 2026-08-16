<!--
reps: 0
priority: 0
-->
#Databases/Transactions #Problems/Persistence #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое dirty read, non-repeatable read, phantom read?**

Dirty: чтение незакоммиченных изменений другой транзакции. Non-repeatable: повторное чтение той же строки даёт другой результат. Phantom: повторный SELECT с WHERE возвращает другое количество строк.

**Dirty / non-repeatable / phantom read — пример каждого.**

Dirty: чтение незакоммиченных данных. Non-repeatable: два чтения одной строки дают разный результат. Phantom: два чтения с WHERE возвращают разное число строк.
