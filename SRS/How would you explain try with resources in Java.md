<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #Java/IO #Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**try-with-resources.**

Автоматически вызывает close() в finally. Ресурс реализует AutoCloseable. Закрытие в обратном порядке объявления. Если и try, и close бросают исключение — close-исключение подавляется (getSuppressed()). С Java 9 можно передать effectively final переменную.

**Что такое try-with-resources?**

Конструкция try (Resource r = ...) {}, которая автоматически вызовет r.close() в finally. Ресурс должен реализовывать AutoCloseable.

**try-with-resources — какой интерфейс нужен?**

AutoCloseable (или Closeable). Ресурсы закрываются автоматически в обратном порядке объявления.

**Что такое try-with-resources?**

Конструкция, которая гарантирует вызов close() у ресурсов, реализующих AutoCloseable. Заменяет try-finally. При исключении в try ресурсы всё равно закроются, а если close() сам бросит — оно станет suppressed внутри основного. try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) { return reader.readLine(); } // reader.close() вызовется автоматически // Даже если упадёт readLine — close всё равно сработает

**try-with-resources — какой интерфейс нужен?**

AutoCloseable (или Closeable). Ресурсы закрываются в обратном порядке.
