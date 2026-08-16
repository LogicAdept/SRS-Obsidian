<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем опасны типы-обёртки (Integer, Boolean)?**

NPE при unboxing null: Integer i = null; int x = i; → NPE. Лишняя память: Integer = 16 байт vs int = 4 байта. Медленнее: автобоксинг создаёт объекты. IntegerCache: valueOf(127) == valueOf(127) → true, valueOf(128) — false. Мораль: для вычислений — примитивы, для коллекций — обёртки.
