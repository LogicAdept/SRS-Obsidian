<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is search_path and why is it a security issue?**

Unqualified names resolve via search_path (often "$user", public). Hijack: attacker creates public.evil shadowing pg_catalog. Set a tight path in migrations; avoid TRUSTED public CREATE. SECURITY DEFINER functions must fix search_path.
