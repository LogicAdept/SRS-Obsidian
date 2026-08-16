<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как установить соединение с базой данных?**

Для установки соединения с базой данных используется статический вызов `java.sql.DriverManager.getConnection(...)` .

В качестве параметра может передаваться:

+ URL базы данных
```java
static Connection getConnection(String url)
```

+ URL базы данных и набор свойств для инициализации
```java
static Connection getConnection(String url, Properties info)
```

+ URL базы данных, имя пользователя и пароль
```java
static Connection getConnection(String url, String user, String password)
```

В результате вызова будет установлено соединение с базой данных и создан объект класса `java.sql.Connection` - своеобразная «сессия», внутри контекста которой и будет происходить дальнейшая работа с базой данных.

**Как закрыть соединение с базой данных?**

Соединение с базой данной закрывается вызовом метода `close()` у соответствующего объекта `java.sql.Connection` или посредством использования механизма try-with-resources при создании такого объекта, появившегося в Java 7.

> __NB!__ Предварительно необходимо закрыть все запросы созданные этим соединением.

# Источники
+ [Википедия - JDBC](https://ru.wikipedia.org/wiki/Java_Database_Connectivity)
+ [IBM developerWorks®](http://www.ibm.com/developerworks/ru/library/dm-1209storedprocedures/)
+ [Документация к пакету java.sql](https://docs.oracle.com/javase/7/docs/api/java/sql/package-summary.html)
+ [Википедия - Уровень изолированности транзакции](https://ru.wikipedia.org/wiki/Уровень_изолированности_транзакций)
