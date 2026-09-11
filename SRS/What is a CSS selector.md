<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/CSS #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В каком порядке выполняются части SELECT-запроса?**

FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT. Это важно: WHERE применяется ДО агрегации, HAVING — после. Алиасы из SELECT можно использовать в ORDER BY, но не в WHERE.
