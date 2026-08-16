<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как мы можем выбрать подходящий бин при помощи application.properties?**

Рассмотрим пример:

````java
interface GreetingService {
    public String sayHello();
}
````

и два компонента

````java
@Component(value="real")
class RealGreetingService implements GreetingService {
    public String sayHello() {
        return "I'm real";
    }
}
````

````java
@Component(value="mock")
class MockGreetingService implements GreetingService {
    public String sayHello() {
        return "I'm mock";
    }
}
````

Тогда в application.properties добавим свойство application.greeting: `real`

Воспользуемся данным решением:

````java
@RestController
public class WelcomeController {
    @Resource(name="${application.greeting}")
    private GreeterService service1;
}
````
