<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое record (Java 14+)?**

Короткий способ описать иммутабельный DTO. Автоматически генерируются: конструктор, геттеры (имя поля без get-), equals, hashCode, toString. record User(String name, int age) {} — всё. Меньше boilerplate, чем Lombok.
