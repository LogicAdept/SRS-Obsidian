<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чем разница между `COUNT(*)` и `COUNT({column})`?**

`COUNT (*)` подсчитывает количество записей в таблице, не игнорируя значение NULL, поскольку эта функция оперирует записями, а не столбцами.

`COUNT ({column})` подсчитывает количество значений в `{column}`. При подсчете количества значений столбца эта форма функции `COUNT` не принимает во внимание значение `NULL`.

**COUNT(*) vs COUNT(col) vs speed?**

COUNT(*) rows; COUNT(col) skips NULL. Neither is free on a huge table. Approximate stats or a counter. COUNT(1) is not a magic speedup in Postgres.
