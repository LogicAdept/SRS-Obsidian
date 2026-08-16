<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Перечислите основные типы данных используемые в JDBC. Как они связаны с типами Java?**

| JDBC Type | Java Object Type |
|---------------:|---------------------------|
| __CHAR__ | `String` |
| __VARCHAR__ | `String` |
| __LONGVARCHAR__ | `String` |
| __NUMERIC__ | `java.math.BigDecimal` |
| __DECIMAL__ | `java.math.BigDecimal` |
| __BIT__ | `Boolean` |
| __TINYINT__ | `Integer` |
| __SMALLINT__ | `Integer` |
| __INTEGER__ | `Integer` |
| __BIGINT__ | `Long` |
| __REAL__ | `Float` |
| __FLOAT__ | `Double` |
| __DOUBLE__ | `Double` |
| __BINARY__ | `byte[]` |
| __VARBINARY__ | `byte[]` |
| __LONGVARBINARY__ | `byte[]` |
| __DATE__ | `java.sql.Date` |
| __TIME__ | `java.sql.Time` |
| __TIMESTAMP__ | `java.sql.Timestamp` |
| __CLOB__ | `Clob` |
| __BLOB__ | `Blob` |
| __ARRAY__ | `Array` |
| __STRUCT__ | `Struct`|
| __REF__ | `Ref` |
| __DISTINCT__ | сопоставление базового типа |
| __JAVA_OBJECT__ | базовый класс Java |
