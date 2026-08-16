<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как воспроизвести OOM?**

static Map без eviction: статический Map, добавляешь объекты в цикле → heap exhaustion. Бесконечное создание Thread: каждый поток = ~1MB стека → native OOM. Metaspace: динамическая генерация классов (CGLIB, ASM). Direct Memory: ByteBuffer.allocateDirect() без освобождения.
