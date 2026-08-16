<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

* **@SpringBootTest for integration testing** 

`@SpringBootTest` tries to mimic the processes added by Spring Boot framework for creating the context e.g. it decides what to scan based on package structures, loads external configurations from predefined locations, optionally runs auto-configuration starters and so on.

```java
@SpringBootTest(webEnvironment=WebEnvironment.RANDOM_PORT)
public class SpringBootDemoApplicationTests 
{   
    @LocalServerPort
    int randomServerPort;
 
    //---- tests -----
}
```
* **@SpringBootTest for unit testing** 

`@SpringBootTest` annotation loads whole application, but it is better to limit Application Context only to a set of spring components that participate in test scenario.

The classes attribute specifies the annotated classes to use for loading an ApplicationContext.
```java
@SpringBootTest(classes = {EmployeeRepository.class, EmployeeService.class})
public class SpringBootDemoApplicationTests 
{   
    @Autowired
    private EmployeeService employeeService;
    //---- tests -----
}
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**@SpringBootTest vs @WebMvcTest vs @DataJpaTest.**

@SpringBootTest: поднимает ВЕСЬ контекст (медленно, для E2E). @WebMvcTest: только контроллеры + MockMvc (без БД). @DataJpaTest: только JPA-слой + встроенная БД. Для AQA: @SpringBootTest + Testcontainers для полных интеграционных тестов.

**@SpringBootTest vs slices?**

Full (or almost full) Boot context. Slow. Use slices (@WebMvcTest, @DataJpaTest) plus @MockBean for unit-speed tests; BootTest + Testcontainers for integration.
