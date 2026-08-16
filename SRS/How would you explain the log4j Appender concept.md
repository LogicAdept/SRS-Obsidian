<!--
reps: 0
priority: 0
-->
#Java/Logging #Java/Library/Log4j #Logging #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**At-least-once vs at-most-once vs exactly-once.**

В реальности чаще at-least-once + идемпотентность на стороне consumer'а. Kafka с transactional producer + read_committed даёт effectively-once.

**Что такое _Appender_ в log4j?**

__Appender__ - это именованный объект журнала событий, реализующий интерфейс `org.apache.log4j.Appender` и добавляющий события в журнал. Appender вызывает разные вспомогательные инструменты - компоновщик, фильтр, обработчик ошибок (если они определены и необходимы). В ходе этой работы окончательно устанавливается необходимость записи сообщения, сообщению придаются окончательные содержание и форма.

В log4j журнал может представлять:

+ консоль;
+ файл;
+ сокет;
+ объект класса реализующего `java.io.Writer` или `java.io.OutputStream`;
+ JDBC хранилище;
+ тему (topic) JMS;
+ NT Event Log;
+ SMTP;
+ Syslog;
+ Telnet.

Наиболее часто используемые log4j appender-ы:

+ `org.apache.log4j.ConsoleAppender` - вывод в консоль;
+ `org.apache.log4j.FileAppender` - добавление в файл;
+ `org.apache.log4j.DailyRollingFileAppender` - добавление в файл с обновлением файла через заданный промежуток времени;
+ `org.apache.log4j.RollingFileAppender` - добавление в файл с обновлением файла по достижению определенного размера;
+ `org.apache.log4j.varia.ExternallyRolledFileAppender` - расширение _RollingFileAppender_ обновляющее файл по команде принятой с заданного порта;
+ `org.apache.log4j.net.SMTPAppender` - сообщение по SMTP;
+ `org.apache.log4j.AsyncAppender` - позволяет, используя отдельный поток, организовать асинхронную работу, когда сообщения фиксируются лишь при достижении определенного уровня заполненности промежуточного буфера.
+ `org.apache.log4j.nt.NTEventLogAppender` - добавление в NT Event Log;
+ `org.apache.log4j.net.SyslogAppender` - добавление в Syslog;
+ `org.apache.log4j.jdbc.JDBCAppender` - запись в хранилище JDBC;
+ `org.apache.log4j.lf5.LF5Appender` - сообщение передаётся в специальный GUI интерфейс LogFactor5
+ `org.apache.log4j.net.SocketAppender` - трансляция сообщения по указанному адресу и порту;
+ `org.apache.log4j.net.SocketHubAppender` - рассылка сообщения сразу нескольким удалённым серверам соединённым по заданному порту;
+ `org.apache.log4j.net.TelnetAppender` - отсылка сообщения по протоколу Telenet;
+ `org.apache.log4j.net.JMSAppender` - добавление сообщения в JMS.
