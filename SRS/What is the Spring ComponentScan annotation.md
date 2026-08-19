<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что делает @ComponentScan?**

Сканирует указанный пакет (по умолчанию — пакет класса, на котором стоит) и все подпакеты на предмет аннотаций @Component, @Service, @Repository, @Controller. Найденные классы регистрируются как бины в контексте.

**Как работает @ComponentScan?**

Сканирует пакеты (по умолчанию — пакет класса с @SpringBootApplication) в поисках @Component, @Service, @Repository, @Controller.

**Для чего нужен Component Scan?**

Первый шаг для описания Spring Beans это добавление аннотации — `@Component`, или `@Service`, или `@Repository`. Однако
Spring ничего не знает об этих бинах, если он не знает где искать их. То, что скажет Spring где искать эти бины и
называется Component Scan. В `@ComponentScan` вы указываете пакеты, которые должны сканироваться. Spring будет искать
бины не только в пакетах для сканирования, но и в их подпакетах.

**What does @ComponentScan do?**

Источник: https://habr.com/ru/articles/967632/

Указывает, где искать @Component/@Service/@Repository/@Controller/@RestController/@Configuration, чтобы создать бины — включая @Bean-методы в конфигурационных классах — и отдать их контейнеру.
