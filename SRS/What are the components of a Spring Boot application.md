<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Boot Framework has mainly four major components.

* **Spring Boot Starters**: The main responsibility of Spring Boot Starter is to combine a group of common or related dependencies into single dependencies. Spring Boot starters can help to reduce the number of manually added dependencies just by adding one dependency. So instead of manually specifying the dependencies just add one starter. Examples are spring-boot-starter-web, spring-boot-starter-test, spring-boot-starter-data-jpa, etc.

* **Spring Boot AutoConfigurator**: One of the common complaint with Spring is, we need to make lot of XML based configurations. Spring Boot AutoConfigurator will simplify all these XML based configurations. It also reduces the number of annotations.

* **Spring Boot CLI**: Spring Boot CLI(Command Line Interface) is a Spring Boot software to run and test Spring Boot applications from command prompt. When we run Spring Boot applications using CLI, then it internally uses Spring Boot Starter and Spring Boot AutoConfigurate components to resolve all dependencies and execute the application.

* **Spring Boot Actuator**: Spring Boot Actuator is a sub-project of Spring Boot. It adds several production grade services to your application with little effort on your part. Actuators enable production-ready features to a Spring Boot application, without having to actually implement these things yourself. The Spring Boot Actuator is mainly used to get the internals of running application like health, metrics, info, dump, environment, etc. which is similar to your production environment monitoring setup.

**How does Spring Boot start the context?**

Источник: https://habr.com/ru/articles/967632/

1) Environment — свойства и профили. 2) ApplicationContext — контейнер бинов. 3) BeanFactory — регистрация бинов. 4) Refresh — lifecycle. 5) Listeners (ApplicationReadyEvent и др.). 6) Embedded server (Tomcat/Jetty), если веб.
