<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое happens-before?**

Отношение в JMM, гарантирующее видимость. Примеры: synchronized release → acquire, volatile write → read, Thread.start() → действия потока, final-поля после конструктора.

**Что такое happens-before?**

Отношение в JMM, гарантирующее видимость операций. Примеры: synchronized release→acquire, volatile write→read, Thread.start→действия потока.

**happens-before: какие пары существуют?**

volatile write → read. synchronized release → acquire. Thread.start() → первая инструкция потока. Последняя инструкция → Thread.join(). final поля после конструктора (если this не утёк). Запись в ConcurrentHashMap → чтение. Без happens-before видимость НЕ гарантирована.

**What is happens-before?**

Источник: https://habr.com/ru/articles/966892/

Правило JMM: если A happens-before B, эффекты A (записи) видны потоку, выполняющему B. Гарантия видимости и порядка, без «плавающих» значений.
