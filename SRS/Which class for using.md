<!--
reps: 0
priority: 0
-->
#Java/IO #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие классы позволяют ускорить чтение/запись за счет использования буфера?**

+ `BufferedInputStream(InputStream in)`/`BufferedInputStream(InputStream in, int size)`,
+ `BufferedOutputStream(OutputStream out)`/`BufferedOutputStream(OutputStream out, int size)`,
+ `BufferedReader(Reader r)`/`BufferedReader(Reader in, int sz)`,
+ `BufferedWriter(Writer out)`/`BufferedWriter(Writer out, int sz)`
