<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**wait/notify — почему while?**

Spurious wakeup: JVM/ОС может разбудить поток без notify. while (!condition) { wait(); }. Важно: вызывать ТОЛЬКО внутри synchronized на том же объекте, иначе — IllegalMonitorStateException. notify() будит один поток, notifyAll() — все.

**Где можно вызывать wait и notify?**

Только внутри synchronized-блока на том же объекте. wait() отпускает монитор, поток засыпает. notify() / notifyAll() — будит. После notify поток должен снова получить монитор, чтобы продолжить. Без synchronized — IllegalMonitorStateException.
