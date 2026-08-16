<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

The core of spring framework is it’s bean factory and mechanisms to create and manage such beans inside Spring container. The beans in spring container can be created in six scopes i.e. singleton, prototype, request, session, application and websocket. They are called spring bean scopes.

|SCOPE | DESCRIPTION |
|-----------------------|-----------------------------------------------------------------------------------------|
|singleton (default) |Single bean object instance per spring IoC container |
|prototype |Opposite to singleton, it produces a new instance each and every time a bean is requested.|
|request |A single instance will be created and available during complete lifecycle of an HTTP request. Only valid in web-aware Spring ApplicationContext.|
|session |A single instance will be created and available during complete lifecycle of an HTTP Session. Only valid in web-aware Spring ApplicationContext.|
|application |A single instance will be created and available during complete lifecycle of ServletContext. Only valid in web-aware Spring ApplicationContext.|
|websocket |A single instance will be created and available during complete lifecycle of WebSocket. Only valid in web-aware Spring ApplicationContext.|

**1. singleton scope**

singleton is default bean scope in spring container. It tells the container to create and manage only one instance of bean class, per container. This single instance is stored in a cache of such singleton beans, and all subsequent requests and references for that named bean return the cached instance.

Example of singleton scope bean using Java config –
```java
@Component
// This statement is redundant - singleton is default scope
@Scope("singleton")  // This statement is redundant
public class BeanClass {
 
}
```
Example of singleton scope bean using XML config –
```xml
<!-- To specify singleton scope is redundant -->
<bean id="beanId" class="com.springexample.BeanClass" scope="singleton" />
// or
<bean id="beanId" class="com.springexample.BeanClass" />
```

**2. prototype scope** 

prototype scope results in the creation of a new bean instance every time a request for the bean is made by application code.

Java config example of prototype bean scope –
```java
@Component
@Scope("prototype")
public class BeanClass {
}
```

XML config example of prototype bean scope –
```xml
<bean id="beanId" class="com.springexample.BeanClass" scope="prototype" />
```

**3. request scope** 

In request scope, container creates a new instance for each and every HTTP request. So, if server is currently handling 5 requests, then container can have at most 5 individual instances of bean class. 

Java config example of request bean scope –
```java
@Component
@Scope("request")
public class BeanClass {
}
 
// or
 
@Component
@RequestScope
public class BeanClass {
}
```

XML config example of request bean scope –
```xml
<bean id="beanId" class="com.springexample.BeanClass" scope="request" />
```

**4. session scope** 

In session scope, container creates a new instance for each and every HTTP session. So, if server has 10 active sessions, then container can have at most 10 individual instances of bean class. All HTTP requests within single session lifetime will have access to same single bean instance in that session scope.

Java config example of session bean scope –
```java
@Component
@Scope("session")
public class BeanClass {
}
 
// or
 
@Component
@SessionScope
public class BeanClass {
}
```

XML config example of session bean scope –
```xml
<bean id="beanId" class="com.springexample.BeanClass" scope="session" />
```

**5. application scope**

In application scope, container creates one instance per web application runtime. It is almost similar to singleton scope, with only two differences i.e.

* application scoped bean is singleton per ServletContext, whereas singleton scoped bean is singleton per ApplicationContext. Please note that there can be multiple application contexts for single application.
* application scoped bean is visible as a ServletContext attribute.

Java config example of application bean scope –
```java
@Component
@Scope("application")
public class BeanClass {
}
 
// or
 
@Component
@ApplicationScope
public class BeanClass {
}
```

XML config example of application bean scope –
```xml
<bean id="beanId" class="com.springexample.BeanClass" scope="application" />
```

**6. websocket scope** 

The WebSocket Protocol enables two-way communication between a client and a remote host that has opted-in to communication with client. WebSocket Protocol provides a single TCP connection for traffic in both directions. 

Java config example of websocket bean scope –
```java
@Component
@Scope("websocket")
public class BeanClass {
}
```

XML config example of websocket bean scope –
```xml
<bean id="beanId" class="com.springexample.BeanClass" scope="websocket" />
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие скоупы бывают у бинов?**

Singleton (default) — один экземпляр на контекст. Prototype — новый объект на каждый запрос get. Request, Session, Application — для веб-приложений. Самое важное: Singleton не потокобезопасен сам по себе — если в нём mutable state, нужна синхронизация.

**What Spring bean scopes exist?**

Источник: https://habr.com/ru/articles/967632/

Singleton (по умолчанию) — один экземпляр на контейнер. Prototype — новый при каждом запросе. Request / Session / Application — веб: HTTP-запрос, сессия, приложение.
