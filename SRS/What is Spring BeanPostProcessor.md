<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое `BeanPostProcessor`?**

Интерфейс `BeanPostProcessor` позволяет вклиниться в процесс настройки ваших бинов до того, как они попадут в контейнер. Интерфейс несет в себе несколько методов.

````java
public interface BeanPostProcessor {
    Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException;

    Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException;
}
````

Оба метода вызываются для каждого бина. У обоих методов параметры абсолютно одинаковые. Разница только в порядке их вызова. Первый вызывается до init-метода, второй, после. Важно понимать, что на данном этапе экземпляр бина уже создан и идет его дополнительная настройка. Тут есть два важных момента:

+ Оба метода в итоге должны вернуть бин. Если в методе вы вернете null, то при получении этого бина из контекста вы получите null, а поскольку через `BeanPostProcessor` проходят все бины, после поднятия контекста, при запросе любого бина вы будете получать фиг, в смысле null.
+ Если вы хотите сделать прокси над вашим объектом, то имейте ввиду, что это принято делать после вызова init метода, иначе говоря это нужно делать в методе `postProcessAfterInitialization`.

Процесс дополнительной настройки показан на рисунке ниже. Порядок в котором будут вызваны BeanPostProcessor не известен,
но мы точно знаем что выполнены они будут последовательно.

**What is BeanPostProcessor?**

Источник: https://habr.com/ru/articles/967632/

BeanPostProcessor перехватывает уже созданный бин перед использованием. На этом основано проксирование, AOP и @Transactional. Порядок: postProcessBeforeInitialization → инициализация → postProcessAfterInitialization.
