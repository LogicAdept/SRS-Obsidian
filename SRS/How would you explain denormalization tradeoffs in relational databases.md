<!--
reps: 0
priority: 0
-->
#Databases/Relational #SystemDesign/Tradeoffs #SystemDesign/Performance #SystemDesign/Scalability #SystemDesign/Consistency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**When can you denormalize a database?**

Источник: https://habr.com/ru/articles/968532/

Сознательно объединяют данные из разных таблиц, чтобы убрать JOIN и ускорить чтение. Когда JOIN — узкое место; высокая нагрузка на SELECT; можно пожертвовать скоростью записи, потому что обновлять денормализованные копии сложнее.
