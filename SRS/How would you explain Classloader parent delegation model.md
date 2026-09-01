<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Classloader: parent delegation model.**

Bootstrap → Platform (ext) → Application. Дочерний сначала делегирует родителю, потом грузит сам.

**How does the ClassLoader delegation model work?**

Источник: https://habr.com/ru/articles/967190/

Delegation Model: ClassLoader сначала делегирует загрузку родителю и только если родитель не нашёл класс, грузит сам. Порядок сверху вниз, чтобы избежать конфликтов и дублирования.
Bootstrap — стандартные классы JDK (rt.jar / модули). Extension/Platform — библиотеки из ext. Application — classpath. Можно написать Custom ClassLoader (OSGi, плагины).
