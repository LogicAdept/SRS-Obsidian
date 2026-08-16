<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What are xmin and xmax?**

Hidden tuple headers. xmin = creating transaction XID. xmax = deleting/updating transaction (or 0 if live). Visibility: a snapshot decides if the tuple is visible. VACUUM can freeze old xmin so wraparound doesn't make rows look in the future.
