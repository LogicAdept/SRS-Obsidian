<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Use `@Qualifier` annotation is used to differentiate beans of the same interface
```java
@SpringBootApplication
public class DemoApplication {

public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
}

public interface MyService {
    void doWork();
}

@Service
@Qualifier("firstService")
public static class FirstServiceImpl implements MyService {

    @Override
    public void doWork() {
        System.out.println("firstService work");
    }
}

@Service
@Qualifier("secondService")
public static class SecondServiceImpl implements MyService {

    @Override
    public void doWork() {
        System.out.println("secondService work");
    }
}

@Component
public static class FirstManager {

    private final MyService myService;

    @Autowired // inject FirstServiceImpl
    public FirstManager(@Qualifier("firstService") MyService myService) {
        this.myService = myService;
    }

    @PostConstruct
    public void startWork() {
        System.out.println("firstManager start work");
        myService.doWork();
    }
}

@Component
public static class SecondManager {

    private final List<MyService> myServices;

    @Autowired // inject MyService all implementations
    public SecondManager(List<MyService> myServices) {
        this.myServices = myServices;
    }

    @PostConstruct
    public void startWork() {
        System.out.println("secondManager start work");
        myServices.forEach(MyService::doWork);
    }
  }
}
```

#### Q. ***What is the use of thymeleaf in spring boot?***
#### Q. ***What is difference between @Controller and @RestController in spring boot?***
#### Q. ***What is the use of servlet initializer in spring boot?***

**How do you inject several beans of the same interface?**

Источник: https://habr.com/ru/articles/967632/

List<PaymentService> — все реализации по порядку. Map<String, PaymentService> — ключи = имена бинов, значения = реализации; можно выбрать по имени.
