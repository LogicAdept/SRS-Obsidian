<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие потокобезопасные коллекции есть в java.util.concurrent?**

ConcurrentHashMap — потокобезопасная HashMap. Не блокирует чтение, на запись — синхронизация по бакету. CopyOnWriteArrayList — копирует весь массив при записи, lock-free на чтение. BlockingQueue — для producer-consumer (put/take блокируют, если очередь полна/пуста).
