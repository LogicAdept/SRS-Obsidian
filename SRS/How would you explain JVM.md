<!--
reps: 0
priority: 0
-->
#Java/JVM #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Области памяти JVM.**

Heap — хранение объектов, управляется GC. Stack — фрейм для каждого вызова метода (локальные переменные, ссылки, примитивы). Metaspace (до Java 8 — PermGen) — метаданные классов, пул интернированных строк. PC Register — адрес текущей инструкции потока. Native Method Stack — для JNI-вызовов.

**Области памяти JVM.**

Heap (объекты), Stack (фреймы методов, примитивы, ссылки), Metaspace (метаданные классов), PC Register, Native Method Stack.

**Области памяти JVM.**

Heap (shared), Stack (per thread), Metaspace (class metadata), PC Register, Native Method Stack.

**Области памяти JVM.**

Heap (Eden/Survivor/Old), Stack (фреймы), Metaspace (метаданные классов, раньше PermGen), PC Register, Native Method Stack, CodeCache (JIT). GC работает только с Heap.

**Области памяти JVM.**

Heap (Eden/Survivor/Old — объекты), Stack (фреймы методов), Metaspace (метаданные классов, раньше PermGen), PC Register, Native Method Stack, CodeCache (JIT-скомпилированный код).
