<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**What is TOAST?**

The Oversized-Attribute Storage Technique: values > ~2KB compressed/out-of-line in a TOAST table. Big JSONB/text don't sit fully in the heap. Updates to other columns can still be HOT; updating the toasted field is expensive. Explains 'small UPDATE, huge WAL' on fat rows.
