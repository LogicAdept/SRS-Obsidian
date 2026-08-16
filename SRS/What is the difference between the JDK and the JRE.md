<!--
reps: 0
priority: 0
-->
#Java/JDK #Java/JRE #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем отличаются JVM, JRE и JDK?**

JVM (Java Virtual Machine) — виртуальная машина, которая исполняет байткод. Содержит GC и JIT-компилятор. JRE (Java Runtime Environment) — JVM + стандартные библиотеки (java.lang, java.util и т.д.), то что нужно для запуска. JDK (Java Development Kit) — JRE + компилятор javac + инструменты (jar, javadoc, jdb). JDK нужен для разработки, JRE — только для запуска.
