<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is off-heap memory in the JVM?**

Источник: https://habr.com/ru/articles/967190/

Память вне стандартного heap, напрямую в native. Пример: ByteBuffer.allocateDirect(). Также пулы нативных ресурсов, кэши больших данных.
JVM эту память не отслеживает как heap — возможны утечки. Неправильное освобождение DirectByteBuffer может дать OutOfMemoryError при пустом heap.
