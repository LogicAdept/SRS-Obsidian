<!--
reps: 0
priority: 0
-->
#Databases/PostgreSQL #Databases/SQL/DataTypes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по PostgreSQL (2026). Не сверен с официальной документацией PostgreSQL. Не считать ответом для ревью.

**numeric vs float for money?**

numeric(p,s) or integer cents. Never float/double for currency. Document the scale. money type is locale-sensitive — usually avoided. Rounding rules belong in the domain, not in IEEE-754.
