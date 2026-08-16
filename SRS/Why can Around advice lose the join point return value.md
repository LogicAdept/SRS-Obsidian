<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Почему возвращаемое значение при применении аспекта `@Around` может потеряться? Назовите причины**

Метод, помеченный аннотацией @Around, должен возвращать значение, которое он (метод) получил из joinpoint.proceed()

````java
@Around("trackTimeAnnotation()")
public Object around(ProceedingJoinPoint joinPoint) throws Throwable{
    long startTime = System.currentTimeMillis();
    Object retVal = joinPoint.proceed();
    long timeTaken = System.currentTimeMillis() - startTime;
    logger.info("Time taken by {} is equal to {}",joinPoint, timeTaken);
    return retVal;
}
````
