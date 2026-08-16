<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Разница между WHERE и HAVING?**

WHERE фильтрует строки ДО группировки и работает с индексами. HAVING — ПОСЛЕ группировки, для условий на агрегаты (HAVING SUM(amount) > 1000).

**В чём разница WHERE и HAVING?**

WHERE фильтрует строки ДО группировки. HAVING — после, по агрегатам. SELECT user_id, COUNT(*) FROM orders WHERE status='OK' GROUP BY user_id HAVING COUNT(*) > 5. По агрегатам (COUNT, SUM) фильтровать в WHERE НЕЛЬЗЯ — они ещё не вычислены.

**WHERE vs HAVING performance?**

WHERE before group — uses indexes, drops rows early. HAVING after aggregate. Don't put non-aggregate filters in HAVING. SELECT alias: WHERE no, ORDER BY yes.
