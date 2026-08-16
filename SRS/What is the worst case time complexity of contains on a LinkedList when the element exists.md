<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CASE WHEN — для условных значений.**

SELECT name, CASE WHEN balance > 100000 THEN 'VIP' WHEN balance > 10000 THEN 'Standard' ELSE 'Basic' END AS category FROM accounts. Для AQA: CASE WHEN удобен в SQL-проверках — классифицировать данные без Java-логики.
