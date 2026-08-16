<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое default-методы в интерфейсах?**

С Java 8 в интерфейсе можно объявить метод с реализацией через ключевое слово default. Это решает проблему расширения интерфейсов без поломки совместимости: добавляешь новый метод с default-реализацией, и существующие реализации не ломаются. Так в Java 8 в Collection появился stream() — default-метод.

**Scope бинов.**

singleton (default), prototype, request, session, application, websocket. Инжект prototype в singleton: через Provider<T>, ObjectFactory<T> или @Lookup. Иначе prototype создастся один раз.
