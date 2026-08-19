<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Напишите простейший многопоточный ограниченный буфер с использованием `ReentrantLock`.**

```java
class QueueReentrantLock<T> {

    private volatile int size = 0;
    private final Object[] content;
    private final int capacity;

    private int out;
    private int in;

    private final ReentrantLock lock = new ReentrantLock();
    private final Condition isEmpty = lock.newCondition();
    private final Condition isFull = lock.newCondition();

    QueueReentrantLock(int capacity) {
        try {
            lock.lock();
            this.capacity = capacity;
            content = new Object[capacity];
            out = 0;
            in = 0;
        } finally {
            lock.unlock();
        }
    }

    private int cycleInc(int index) {
        return (++index == capacity)
                ? 0
                : index;
    }

    @SuppressWarnings("unchecked")
    T get() throws InterruptedException {
        try {
            lock.lockInterruptibly();
            if (size == 0) {
                while (size < 1) {
                    isEmpty.await();
                }
            }
            final Object value = content[out];
            content[out] = null;
            if (size > 1) {
                out = cycleInc(out);
            }
            size--;
            isFull.signal();
            return (T) value;
        } finally {
            lock.unlock();
        }
    }

    QueueReentrantLock<T> put(T value) throws InterruptedException {
        try {
            lock.lockInterruptibly();
            if (size == capacity) {
                while (size == capacity) {
                    isFull.await();
                }
            }
            if (size == 0) {
                content[in] = value;
            } else {
                in = cycleInc(in);
                content[in] = value;
            }
            size++;
            isEmpty.signal();
        } finally {
            lock.unlock();
        }
        return this;
    }
}
```

# Источники
+ [Хабрахабр - Многопоточность в Java](https://habrahabr.ru/post/164487/)
+ [IBM DeveloperWorks - Выполнение задач в многопоточном режиме](https://www.ibm.com/developerworks/ru/library/l-java_universe_multithreading_tasks/)
+ [Записки трезвого практика](http://www.skipy.ru/technics/synchronization.html)
+ [IBM DeveloperWorks - SCJP](https://www.ibm.com/developerworks/ru/edu/j-scjp/section8.html)
+ [JavaRush](http://info.javarush.ru/KapChook/2015/02/15/Перевод-Топ-50-интервью-вопросов-по-нитям-Часть-1-.html)
+ [Хабрахабр - Справочник по синхронизаторам `java.util.concurrent.*`](https://habrahabr.ru/post/277669/)
+ [Блог сурового челябинского программиста](http://samolisov.blogspot.ru/2011/04/threadlocal.html)
+ [IBM DeveloperWorks - Более гибкая, масштабируемая блокировка в JDK 5.0](http://www.ibm.com/developerworks/ru/library/j-jtp10264/)
+ [Хабрахабр - Правильный Singleton в Java](https://habrahabr.ru/post/129494/)
+ [duct-tape-architect.ru](http://www.duct-tape-architect.ru/?p=294#3__171_187___Java_HotSpot_JVM6)
