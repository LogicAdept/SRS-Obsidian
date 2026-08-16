<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Напишите потокобезопасную реализацию класса с неблокирующим методом `BigInteger next()`, который возвращает элементы последовательности: `[1, 2, 4, 8, 16, ...]`.**

```java
class PowerOfTwo {
    private AtomicReference<BigInteger> current = new AtomicReference<>(null);

    BigInteger next() {
        BigInteger recent, next;
        do {
            recent = current.get();
            next = (recent == null) ? BigInteger.valueOf(1) : recent.shiftLeft(1);
        } while (!current.compareAndSet(recent, next));
        return next;
    }
}
```
