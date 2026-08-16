<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое `ReadWriteLock`?**

`ReadWriteLock` – это интерфейс расширяющий базовый интерфейс `Lock`. Используется для улучшения производительности в многопоточном процессе и оперирует парой связанных блокировок (одна - для операций чтения, другая - для записи). Блокировка чтения может удерживаться одновременно несколькими читающими потоками, до тех пор пока не появится записывающий. Блокировка записи является эксклюзивной.

Существует реализующий интерфейс `ReadWriteLock` класс `ReentrantReadWriteLock`, который поддерживает до 65535 блокировок записи и до стольки же блокировок чтения.

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock rLock = rwLock.readLock();
Lock wLock = rwLock.writeLock();

wLock.lock();
try {
    // exclusive write
} finally {
    wLock.unlock();
}

rLock.lock();
try {
    // shared reading
} finally {
    rLock.unlock();
}
```
