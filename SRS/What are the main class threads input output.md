<!--
reps: 0
priority: 0
-->
#Java/IO #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Назовите основные классы потоков ввода/вывода.**

Разделяют два вида потоков ввода/вывода:

+ __байтовые__ - `java.io.InputStream`, `java.io.OutputStream`;
+ __символьные__ - `java.io.Reader`, `java.io.Writer`.

**В каких пакетах расположены классы потоков ввода/вывода?**

`java.io`, `java.nio`. Для работы с потоками компрессированных данных используются классы из пакета `java.util.zip`

**Какие классы поддерживают чтение и запись потоков в компрессированном формате?**

+ `DeflaterOutputStream` - компрессия данных в формате deflate.
+ `Deflater` - компрессия данных в формат ZLIB
+ `ZipOutputStream` - потомок `DeflaterOutputStream` для компрессии данных в формат Zip.
+ `GZIPOutputStream` - потомок `DeflaterOutputStream` для компрессии данных в формат GZIP.
+ `InflaterInputStream` - декомпрессия данных в формате deflate.
+ `Inflater` - декомпрессия данных в формате ZLIB
+ `ZipInputStream` - потомок `InflaterInputStream` для декомпрессии данных в формате Zip.
+ `GZIPInputStream` - потомок `InflaterInputStream` для декомпрессии данных в формате GZIP.
