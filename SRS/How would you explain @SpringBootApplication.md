<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**@SpringBootApplication.**

@Configuration + @EnableAutoConfiguration + @ComponentScan. Автоконфигурация через @Conditional: если DataSource в classpath — настроит JPA. Список в META- INF/spring/...AutoConfiguration.imports (Spring Boot 3+, раньше spring.factories).

**Что делает @SpringBootApplication?**

Это композиция трёх аннотаций: @Configuration + @EnableAutoConfiguration + @ComponentScan.

**Что делает @SpringBootApplication?**

Это композиция трёх: @Configuration + @EnableAutoConfiguration + @ComponentScan.

**@SpringBootApplication.**

@Configuration + @EnableAutoConfiguration + @ComponentScan.

**@SpringBootApplication.**

@Configuration + @EnableAutoConfiguration + @ComponentScan.

**Как вы добавите Component Scan в Spring Boot?**

````java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
````

`@SpringBootApplication` определяет автоматическое сканирование пакета, где находится класс Application.

**What does @SpringBootApplication include?**

Источник: https://habr.com/ru/articles/967632/

@SpringBootConfiguration + @EnableAutoConfiguration + @ComponentScan (с exclude-фильтрами TypeExcludeFilter и AutoConfigurationExcludeFilter).

**Three annotations in @SpringBootApplication?**

@SpringBootConfiguration + @EnableAutoConfiguration + @ComponentScan (with Boot exclude filters).
