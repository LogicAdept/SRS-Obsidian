<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

* **@Component**
This is a general-purpose stereotype annotation indicating that the class is a spring component.
```java
@Component
public @interface Service {
    ….
}
```
* **@Repository**
This is to indicate that the class defines a database repository.
```xml
<bean class="org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor"/>
```
* **@Controller**
This indicate that the annotate classes at presentation layers level, mainly used in Spring MVC.

* **@Service**
 @Service beans hold the business logic and call methods in the repository layer.

![alt text](https://github.com/learning-zone/spring-interview-questions/blob/spring/assets/spring-component.png)

**В чём разница между `@Component`, `@Service` и `@Repository` аннотациями?**

Все они определяют бины Spring. Однако между ними всё же есть разница.

`@Component` — универсальный компонент
`@Repository` — компонент, который предназначен для хранения, извлечения и поиска. Как правило, используется для работы с базами данных.
`@Service` — фасад для некоторой бизнес логики

Пользовательские аннотации, производные от @Component, могут добавлять специальную логику в бинах.
Например, бины, получившиеся при помощи @Repository, дополнительно имеют обработку для JDBC Exception
