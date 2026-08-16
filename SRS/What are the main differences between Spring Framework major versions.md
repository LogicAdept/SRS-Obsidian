<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие основные отличия в версиях Spring?**

+ __Версия 3 (2009)__ - Поддержка Java 5 (annotations, generics, varargs, ...).
+ __Версия 4 (2016)__ - Поддержка Java 8 (lambda, stream api, ...).
+ __Версия 5 (2017)__ - Построен на основе `Reactive Streams`.

**Какие основные отличия в версиях Java?**

##### Версия 1.0 - 23 января 1996.

##### Версия 1.1 - 19 февраля 1997.
+ __Inner Classes__.
+ __Reflection API__.
+ __JavaBeans__.
+ __JDBC__.
+ __Collections framework__.

##### Версия 1.2 - 8 декабря 1998.
+ __`strictfp` keyword__.
+ __JDBC__.

##### Версия 1.3 - 8 мая 2000.
+ __HotSpot VM included__.

##### Версия 1.4 - 6 февраля 2002.
+ __`assert` keyword__.
+ __NIO.2 library__  - API для работы с неблокирующим вводом-выводом.
+ __Logging API__.

##### Версия 5 - 30 сентября 2004 года.
+ __Enum__ - перечислимые типы.
+ __Annotations__ - аннотации, специальные интерфейсы.
+ __Generics__ - средства обобщённого программирования.
+ __Varargs__ - методы с неопределённым числом параметров.
+ __Autoboxing/Unboxing__ — автоматическое преобразование между скалярными типами Java и соответствующими типами-обёртками.
+ __Static import__ - импорт статических полей и методов.
+ __Foreach__ - итератор по коллекции объектов.
+ __Javadoc comments__ - Javadoc-комментариев.

##### Версия 6 - 11 декабря 2006 года.
+ __Scripting Language Support__ - общий API для скриптовых языков и встроенный JS-движок Mozilla Rhino.
+ __JDBC 4.0__.
+ __Java Compiler API__ - возможность программного вызова java-компилятора.
+ __JAXB 2.0__.
+ __PLuggable Annotations__.
+ __@Override__ - использование аннотации для маркирования методов, реализующих интерфейс или расширяющих родительский класс.

##### Версия 7 - 7 июля 2011 года.
+ __InvokeDynamic__ - поддержка динамических языков программирования.
+ __Strings in switch__. - строки в switch-выражениях.
+ __The try-with-resources statement__ - автоматическое управление ресурсами, реализующими интерфейс java.lang.AutoCloseable.
+ __Diamond operator <>__ - улучшенное вычисление типов при создании обобщенных экземпляров.
+ __Simplified varargs method declaration__ - перенос предупреждения "unsafe operation" вместо объявления метода с переменным количеством аргументов.
+ __Binary integer literals__ - префикс _0b_ (int i = 0b0101)
+ __Underscores in numeric literals__ - подчеркивания в числах (int i = 1_000)
+ __Catching multiple exception types__ - перехват нескольких типов исключений в одном блоке catch (catch(SQLException | IOException e)).
+ __DualPivotQuickSort__ - в качестве стандартного алгоритма для сортировки примитивов.
+ __TimSort__ - в качестве стандартного алгоритма для сортировки объектов.
+ __Concurrency utilities__ - новый синхронизатор Phaser, включён легковесный механизм fork/join.
+ __NIO.2 library__ - добавлены пакеты java.nio.file, java.nio.file.attribute и java.nio.file.spi.

##### Версия 8 - 18 марта 2014 года.
+ __Lambda expressions__ - выражения в функциональном стиле.
+ __@FunctionalInterface__ - функциональные интерфейсы.
+ __Stream API__. - возможность выполнения последовательности операций над элементами массива, а также возможность производить их параллельно (parallelStream).
+ __Method Reference__ - ссылки на методы и конструкторы, оператор `::`.
+ __Repeatable annotations__ - возможность использовать аннотации одного типа несколько раз над одним объектом.
+ __Interface default method__ - методы по умолчанию для интерфейсов.
+ __Annotation on Java types__ - аннотации на типы данных.
+ __Reflection for method parameters__ - рефлексия для параметров методов.
+ __Date & Time API (java.time)__ - новое api для работы с датами и временем.
+ __Remove the PermGen__ - удален _PermGen_, изменен способ хранения мета-данных классов.

##### Версия 9 - 21 сентября 2017 года.
+ __HTTP/2 support__.
+ __Jshell__ - поддержка REPL-подхода (Read-Eval-Print-Loop) в Java.
+ __JigSaw project__ - поддержка модуляризации в Java.
+ __Stream API updates__.
+ __Immutable collevtions__ - создании и инициализация коллекций в одну строку.
+ __Concurrency updates__ - реализация Reactive Streams (в т.ч. класс `Flow`).
+ __class Optional__  - класс для сбора not-null объектов.
+ __Complete the removal of underscore from the set of legal identifier names__ - запрет подчёркивания в именах классов.
+ __Support for private methods in interfaces__- private и static private методы в интерфейсах.
+ __Compact strings__ - хранение строк в кодировке LATIN-1, если это возможно.

##### Версия 10 - 20 марта 2018 года.
+ __ Local-variable type inference__ - ключевое слово `var`, что избавляет от необходимости указывать тип локальной переменной явно.
+ __Stream API updates__.
+ __Concurrency updates__.

##### Версия 11 - 25 сентября 2018 года.
+ __Local-Variable Syntax for Lambda Parameters__ - ключевое слово `var` в локальных Лямбда-переменных, например при использовании аннотаций.
+ __Launch Single-File Source-Code Programs__ - запуск приложения одной командой `java HelloWorld.java`.
+ __Remove The Java EE and CORBA Modules__ — удалены модули Java EE и COBRA.

##### Версия 12 - 19 марта 2019 года.
+ __Switch Expressions__ - новая форма метки switch “case L ->” чтобы очевидным образом показать, что будет выполняться только код справа от метки, если эта метка – подходящая.

##### Версия 13 - 17 сентября 2019 года.
+ __Text Blocks__ - Использование `"""` для создания текстовых блоков без экранирования спец. символов.
+ __Reimplement the legacy Socket API__ - новая реализацию `NioSocketImpl`. Она больше не требует нативного кода, тем самым упрощая перенос на разные платформы.

##### Версия 14 - 17 марта 2020 года.
+ __Records__ - записи похожи на перечисления и позволяют упростить код. По сути, они заменяют классы, у которых есть состояние, но нет поведения - есть поля, нет методов.
+ __Pattern Matching for instanceof__.
+ __Remove the Concurrent Mark Sweep (CMS) Garbage Collector__.
