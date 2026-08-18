<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What are window functions?**

ROW_NUMBER/RANK/SUM() OVER (PARTITION BY ... ORDER BY ...). Compute aggregates without collapsing rows. LAG/LEAD for previous row. Frame (ROWS BETWEEN). Interview: latest per group = ROW_NUMBER()=1 vs DISTINCT ON.

**Window vs correlated subquery?**

ROW_NUMBER for latest-per-group in one pass. Can still sort a huge partition — pair with a supporting index or prefilter. Not a search index; it's a compute shape.
