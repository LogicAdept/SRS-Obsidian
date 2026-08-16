<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #Logging #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

In Spring Boot, Logback is the default logging framework, just add spring-boot-starter-web, it will pull in the logback dependencies. 
**pom.xml** 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
		 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <artifactId>spring-boot-slf4j</artifactId>
    <packaging>jar</packaging>
    <name>Spring Boot SLF4j</name>
    <version>1.0</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.1.2.RELEASE</version>
    </parent>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <!-- Package as an executable jar/war -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>2.22.0</version>
            </plugin>
        </plugins>
    </build>
</project>
```
* **application.properties**
```
# logging level
logging.level.org.springframework=ERROR
logging.level.com.mkyong=DEBUG

# output to a file
logging.file=app.log

# temp folder example
#logging.file=${java.io.tmpdir}/app.log

logging.pattern.file=%d %p %c{1.} [%t] %m%n

logging.pattern.console=%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n

## if no active profile, default is 'default'
##spring.profiles.active=prod

# root level
#logging.level.=INFO
```
* **logback.xml**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>

    <property name="HOME_LOG" value="logs/app.log"/>

    <appender name="FILE-ROLLING" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${HOME_LOG}</file>

        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>logs/archived/app.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <!-- each archived file, size max 10MB -->
            <maxFileSize>10MB</maxFileSize>
            <!-- total size of all archive files, if total size > 20GB, 
				it will delete old archived file -->
            <totalSizeCap>20GB</totalSizeCap>
            <!-- 60 days to keep -->
            <maxHistory>60</maxHistory>
        </rollingPolicy>

        <encoder>
            <pattern>%d %p %c{1.} [%t] %m%n</pattern>
        </encoder>
    </appender>

    <logger name="com.mkyong" level="debug" additivity="false">
        <appender-ref ref="FILE-ROLLING"/>
    </logger>

    <root level="error">
        <appender-ref ref="FILE-ROLLING"/>
    </root>

</configuration>
```

**HelloController.java**
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import java.util.Arrays;
import java.util.List;

@Controller
public class HelloController {

    private static final Logger logger = LoggerFactory.getLogger(HelloController.class);

    @GetMapping("/")
    public String hello(Model model) {

        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);

        logger.debug("Hello from Logback {}", data);
        model.addAttribute("num", data);

        return "index"; // index.html
    }
}
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое Spring Boot и чем он отличается от Spring?**

Spring Boot — это Spring + автоконфигурация + встроенный сервер (Tomcat/Jetty) + удобные стартеры. Минимизирует boilerplate. По сути «Spring без боли с XML».

**Что такое стартер в Spring Boot?**

Готовый набор зависимостей под задачу. Например, spring-boot-starter-web подтянет Spring MVC, Tomcat, Jackson и т.д. Один импорт — и веб-приложение работает.

**Как Spring Boot узнаёт, что и как настраивать?**

Через @EnableAutoConfiguration (входит в @SpringBootApplication) + @Conditional. Конфигурации перечислены в META-INF/spring/...AutoConfiguration.imports (или старом spring.factories).

**Что такое Spring Boot?**

Spring + автоконфигурация + встроенный сервер (Tomcat/Jetty/Undertow) + стартеры. Минимизирует boilerplate.

**В чём плюшка Spring Boot?**

Автоконфигурация — Spring Boot сам подключает компоненты в зависимости от того, что есть на classpath. Стартеры — готовые наборы зависимостей (spring-boot-starter-web подтягивает Spring MVC, Tomcat, Jackson). Встроенный веб-сервер (Tomcat). Минимум конфигурации в XML, всё через свойства и аннотации.

**Какие аннотации для тестов в Spring Boot?**

@SpringBootTest — поднимает весь контекст приложения. Долго, но полноценно. @WebMvcTest — только web-слой (контроллеры), без БД. @DataJpaTest — только JPA-слой, с in-memory БД. MockMvc — имитация HTTP-запросов в тестах.

**Spring Boot 3 + Java 21.**

GraalVM native image, Virtual Threads support (spring.threads.virtual.enabled=true), Jakarta EE вместо javax.
