<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

* **@SpringBootApplication**: annotation is used to annotate the main class of our Spring Boot application. It also enables the auto-configuration feature of Spring Boot.
```java
@SpringBootApplication
public class SpringBootDemo {
   public static void main(String args[]) {
      SpringApplication.run(SpringBootDemo.class, args);
   }
}
```
* **@EnableAutoConfiguration**: The auto-configuration feature automatically configures things if certain classes are present in the Classpath. For example, if you have a data source bean present in the classpath of the application, then it automatically configures the JDBC template. 
```java
@Configuration
@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class})
public class SpringBootDemo {
  //.. Java code
}
```

**Auto-config 2026 detail?**

Classpath starter → AutoConfiguration.imports → @ConditionalOnClass/OnMissingBean/OnProperty. User beans override. --debug shows the report.
