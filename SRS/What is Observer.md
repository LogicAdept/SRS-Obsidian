<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое Observer?**

Поведенческий паттерн: один объект (Subject) хранит список подписчиков (Observer), при изменении состояния — уведомляет всех. В Java встречается: PropertyChangeListener, java.util.Observer (устарел), Spring Events, RxJava. Все системы событий — это Observer. interface EventListener { void onEvent(Event e); }
