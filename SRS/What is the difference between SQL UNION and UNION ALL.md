<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чём разница UNION и UNION ALL?**

UNION — объединяет результаты ДВУХ SELECT, убирает дубликаты. UNION ALL — то же, но БЕЗ удаления дубликатов. UNION ALL быстрее (не нужно сортировать для дедупликации). Если знаешь, что дублей не будет — всегда UNION ALL.

**UNION cost?**

UNION sorts/hashes to unique. ALL is cheaper. Split OR into UNION ALL of indexed seeks. DISTINCT same family of cost as UNION.
