<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Debugging #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Чтобы сделать heap dump на запущенном приложении:

С помощью команды `jps` узнаём id процесса

Вызываем heap dump текущего состояния

```bash
jcmd 87777 GC.heap_dump ~/Documents/heapDumpс.hprof
```

Далее этот heap dump файл можно открыть в profiler в IDEA

Чтобы сделать heap dump при остановке приложения:

В VM options нужно добавить флаг `-XX:+HeapDumpOnOutOfMemoryError`

Так, при остановке приложения с ошибкой OutOfMemoryError рядом появится файл heap dump. Важно, этот файл в размере от 1 гигабайта и более, на сервере должно быть свободно место.
