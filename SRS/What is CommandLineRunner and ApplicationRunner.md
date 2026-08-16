<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

`ApplicationRunner` and `CommandLineRunner` interfaces use to execute the code after the Spring Boot application is started. These interfaces can be used to perform any actions immediately after the application has started.

* **CommandLineRunner**
This interface provides access to application arguments as string array. 
```java
@Component
public class CommandLineAppStartupRunner implements CommandLineRunner {
    private static final Logger logger = LoggerFactory.getLogger(CommandLineAppStartupRunner.class);
    @Override
    public void run(String...args) throws Exception {
        logger.info("Application started with command-line arguments: {} . 
        \n To kill this application, press Ctrl + C.", Arrays.toString(args));
    }
}
```
* **ApplicationRunner**
ApplicationRunner wraps the raw application arguments and exposes the ApplicationArguments interface, which has many convinent methods to get arguments, like getOptionNames() to return all the arguments' names, getOptionValues() to return the agrument value, and raw source arguments with method getSourceArgs(). 
```java
@Component
public class AppStartupRunner implements ApplicationRunner {
    private static final Logger logger = LoggerFactory.getLogger(AppStartupRunner.class);
    @Override
    public void run(ApplicationArguments args) throws Exception {
        logger.info("Your application started with option names : {}", args.getOptionNames());
    }
}
```
