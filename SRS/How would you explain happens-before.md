<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**happens-before.**

Ключевое отношение JMM. Если A happens-before B, то записи в A видны в B. Примеры: unlock → lock того же монитора. volatile write → read. Thread.start() → первая инструкция потока. Последняя инструкция → Thread.join(). final-поля видны после конструктора.

**happens-before.**

unlock → lock. volatile write → read. Thread.start() → первая инструкция. join(). final-поля после конструктора.

**happens-before.**

unlock → lock того же монитора. volatile write → read. Thread.start() → первая инструкция потока. Последняя инструкция → join(). final-поля видны после конструктора.
