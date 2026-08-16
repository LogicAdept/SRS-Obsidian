<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**synchronized.**

Захватывает монитор объекта. Instance-метод — монитор this. Static — монитор Class. Блок — указанный объект. Только один поток. Reentrant: поток может повторно захватить свой монитор (счётчик). Гарантирует: mutual exclusion + happens-before (видимость).

**synchronized.**

Захват монитора. Instance → this. Static → Class. Reentrant (счётчик). Mutual exclusion + happens-before.

**synchronized.**

Захват монитора. Instance-метод → this. Static → Class. Блок → указанный объект. Reentrant (счётчик). Гарантирует: mutual exclusion + happens-before (видимость).

**How does synchronized work?**

Источник: https://habr.com/ru/articles/966892/

На уровне instance-метода, static-метода или блока. Монитор привязан к объекту: один поток на этот монитор. Static synchronized — монитор Class; один поток на класс независимо от числа экземпляров. Блок synchronized(this) или ClassName.class для static.
