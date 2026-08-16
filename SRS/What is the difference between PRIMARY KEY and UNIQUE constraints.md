<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**PRIMARY KEY vs UNIQUE — отличия.**

PRIMARY KEY: уникальность + NOT NULL + один на таблицу + кластерный индекс. UNIQUE: уникальность (допускает один NULL) + может быть несколько. Foreign Key ссылается на PRIMARY KEY (или UNIQUE).

**В чём разница PRIMARY KEY и UNIQUE?**

PRIMARY KEY — один на таблицу, NOT NULL. UNIQUE — может быть несколько UNIQUE-индексов, разрешает NULL (NULL не равно NULL, поэтому много NULL допустимо).
