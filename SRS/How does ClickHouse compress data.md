<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**Codecs and compression?**

Column codecs (LZ4 default, ZSTD, Delta/DoubleDelta/Gorilla for time series) then compressor. Sorted low-cardinality columns compress best — another reason ORDER BY matters. Trade CPU vs disk. Fat uncompressible blobs (already compressed JSON) gain little.
