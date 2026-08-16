<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring AOP enables Aspect-Oriented Programming in spring applications. In AOP, aspects enable the modularization of concerns such as transaction management, logging or security that cut across multiple types and objects (often termed crosscutting concerns).

AOP provides the way to dynamically add the cross-cutting concern before, after or around the actual logic using simple pluggable configurations. It makes easy to maintain code in the present and future as well.

* **Aspect Oriented Programming Core Concepts**

1. **Aspect**: An aspect is a class that implements enterprise application concerns that cut across multiple classes, such as transaction management. 

2. **Join Point**: A join point is the specific point in the application such as method execution, exception handling, changing object variable values etc. In Spring AOP a join points is always the execution of a method.

3. **Advice**: Advices are actions taken for a particular join point. In terms of programming, they are methods that gets executed when a certain join point with matching pointcut is reached in the application.

4. **Pointcut**: Pointcut are expressions that is matched with join points to determine whether advice needs to be executed or not. Pointcut uses different kinds of expressions that are matched with the join points and Spring framework uses the AspectJ pointcut expression language.

5. **Weaving**: It is the process of linking aspects with other objects to create the advised proxy objects. This can be done at compile time, load time or at runtime. Spring AOP performs weaving at the runtime.

* **Types of Advices**

1. **Before Advice**: These advices runs before the execution of join point methods. We can use @Before annotation to mark an advice type as Before advice.

2. **After returning advice**: Advice to be executed after a join point completes normally: for example, if a method returns without throwing an exception.

3. **After throwing advice**: Advice to be executed if a method exits by throwing an exception.

4. **After advice**: Advice to be executed regardless of the means by which a join point exits.

5. **Around advice**: Around advice can perform custom behavior before and after the method invocation. This type of advice is used where we need frequent access to a method or database like- caching.

Example: Types of Advices 
```java
/**
* AOP program to illustrate types of Advices
*
*// 
@Aspect
class Logging { 
    
    // **Before** 
    @Before("execution(public void com.aspect.ImplementAspect.aspectCall())") 
    public void loggingAdvice1() { 
        System.out.println("Before advice is executed"); 
    } 
  
    // **After** 
    @After("execution(public void com.aspect.ImplementAspect.aspectCall())") 
    public void loggingAdvice2() { 
        System.out.println("Running After Advice."); 
    } 
  
    // **Around** 
    @Around("execution(public void com.aspect.ImplementAspect.myMethod())") 
    public void loggingAdvice3() { 
        System.out.println("Before and After invoking method myMethod"); 
    } 
  
    // **AfterThrowing** 
    @AfterThrowing("execution(" public void com.aspect.ImplementAspect.aspectCall())") 
    public void loggingAdvice4() { 
        System.out.println("Exception thrown in method"); 
    } 
  
    // **AfterRunning** 
    @AfterReturning("execution(public void com.aspect.ImplementAspect.myMethod())") 
    public void loggingAdvice5() { 
        System.out.println("AfterReturning advice is run"); 
    } 
}
```

Example: JoinPoints
```java
/**
* AOP program to illustrate JoinPoints
*
**/
  
@Aspect
class Logging { 
  
    // Passing a JoinPoint Object into parameters of the method 
    // with the annotated advice enables to print the information 
  
    @Before("execution(public void com.aspect.ImplementAspect.aspectCall())") 
    public void loggingAdvice1(JoinPoint joinpoint) { 
        System.out.println("Before advice is executed"); 
        System.out.println(joinpoint.toString()); 
    } 
} 
```
Example: PointCuts 
```java
/**
* AOP program to illustrate PointCuts 
*
**/
@Aspect
class Logging { 

    @Pointcut("execution(public void com.aspect.ImplementAspect.aspectCall())") 
    public void pointCut() { 
    } 
  
    // pointcut() is used to avoid repeatition of code 
    @Before("pointcut()") 
    public void loggingAdvice1() { 
        System.out.println("Before advice is executed"); 
    } 
} 
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**AOP: кейс «замерить время всех методов сервиса».**

@Aspect + @Around("execution(* com.example.service.*.*(..))"). ProceedingJoinPoint: long start = System.nanoTime(); Object result = pjp.proceed(); long elapsed = System.nanoTime() - start; log.info("{} took {} ms", methodName, elapsed/1_000_000); return result. В проде: Micrometer @Timed вместо ручного AOP.

**AOP: JDK proxy vs CGLIB.**

JDK dynamic proxy — если бин реализует интерфейс (через Proxy.newProxyInstance). CGLIB — наследование от класса (final-классы нельзя проксировать). Spring Boot 3 по умолчанию использует CGLIB.

**В чем разница между Сквозной Функциональностью (Cross Cutting Concerns) и АОП (аспектно ориентированное программирование)?**

Сквозная Функциональность — функциональность, которая может потребоваться вам на нескольких различных уровнях —
логирование, управление производительностью, безопасность и т.д.
АОП — один из подходов к реализации данной проблемы

**What is Spring AOP?**

Источник: https://habr.com/ru/articles/967632/

Выносит повторяющееся (логирование, транзакции, безопасность) в аспекты, не смешивая с бизнес-логикой. Аспект = advice (код до/после/вокруг метода) + pointcut (где применять).

**AOP terms interviewers want?**

Aspect = pointcut + advice. Join point = method execution in Spring AOP. @Transactional/@Cacheable/@Async/@PreAuthorize are aspects.
