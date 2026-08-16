<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is fillfactor?**

Percent of page to fill on INSERT (default 100). Lower (e.g. 80–90) leaves room for HOT updates on update-heavy tables. Trade: more space, fewer random heap inserts on UPDATE. Useless if you always update indexed columns.
