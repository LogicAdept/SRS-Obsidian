<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как реализовать потокобезопасный singleton?**

Лучший вариант — enum. Альтернативы: static holder (Initialization-on-demand), double-checked locking с volatile.

**Что такое Singleton?**

Гарантирует, что в системе будет один экземпляр класса, и даёт глобальную точку доступа. Используется для конфигов, логгеров, пулов соединений. В Spring каждый @Component по умолчанию — Singleton.

**Как реализовать Singleton?**

Самый простой и правильный способ — через enum (с Java 5): public enum Database { INSTANCE; public void connect() { /* ... */ } }

**Как сделать потокобезопасный singleton?**

Лучшее — enum. Альтернативы: static holder (lazy init via classloader), double-checked locking с volatile.

**Singleton-бин: потокобезопасен ли?**

НЕТ. Singleton означает один экземпляр на контекст, но это НЕ делает его потокобезопасным. Если есть mutable state (поля, не final) — race condition. Решения: stateless бины (без полей-состояний), ThreadLocal, synchronized, ConcurrentHashMap. В Spring MVC: контроллеры и сервисы — singleton, но stateless.

**Что такое _double checked locking Singleton_?**

__double checked locking Singleton__ - это один из способов создания потокобезопасного класса реализующего шаблон Одиночка. Данный метод пытается оптимизировать производительность, блокируясь только случае, когда экземпляр одиночки создаётся впервые.

```java
class DoubleCheckedLockingSingleton {
    private static volatile DoubleCheckedLockingSingleton instance;

    static DoubleCheckedLockingSingleton getInstance() {
        DoubleCheckedLockingSingleton current = instance;
        if (current == null) {
            synchronized (DoubleCheckedLockingSingleton.class) {
                current = instance;

                if (current == null) {
                    instance = current = new DoubleCheckedLockingSingleton();
                }
            }
        }
        return current;
    }
}
```

Следует заметить, что требование `volatile` обязательно. Проблема Double Checked Lock заключается в модели памяти Java, точнее в порядке создания объектов, когда возможна ситуация, при которой другой поток может получить и начать использовать (на основании условия, что указатель не нулевой) не полностью сконструированный объект. Хотя эта проблема была частично решена в JDK 1.5, однако рекомендация использовать `voloatile` для Double Checked Lock остаётся в силе.
