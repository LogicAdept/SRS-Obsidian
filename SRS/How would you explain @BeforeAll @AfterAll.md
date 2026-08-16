<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**@BeforeAll и @AfterAll — что важно?**

В JUnit 5 они должны быть static (или класс аннотирован @TestInstance(Lifecycle.PER_CLASS)).
