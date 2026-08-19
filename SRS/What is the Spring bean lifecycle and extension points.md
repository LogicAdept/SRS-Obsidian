<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как происходит запуск IoC-контейнера Spring?**

1. __Парсинг конфигурации и создание BeanDefinition__ - конфигурация с помощью XNL, аннотаций, JavaConfig.
2. __Настройка созданных BeanDefinition__ - на данном этапе происходит настройка еще не созданных бинов через классы, реализующие `BeanFactoryPostProcessor`. Например, `PropertySourcesPlaceholderConfigurer`
3. __Создание кастомных FactoryBean__ - `FactoryBean` — это generic интерфейс, которому можно делегировать процесс создания бинов.
4. __Создание экземпляров бинов__ - созданием экземпляров бинов занимается `BeanFactory` при этом, если нужно, делегирует это кастомным `FactoryBean`. Экземпляры бинов создаются на основе ранее созданных `BeanDefinition`.
5. __Настройка созданных бинов__ - Интерфейс `BeanPostProcessor` позволяет вклиниться в процесс настройки ваших бинов до того, как они попадут в контейнер. Интерфейс несет в себе несколько методов.

**What is the Spring bean lifecycle?**

Источник: https://habr.com/ru/articles/967632/

1) Создание объекта. 2) Заполнение зависимостями (DI). 3) Инициализация: @PostConstruct, initMethod у @Bean. 4) Уничтожение: @PreDestroy, destroyMethod у @Bean.

**Where are AOP proxies created in the lifecycle?**

Instantiate → inject → Aware → BPP before → @PostConstruct / afterPropertiesSet / init-method → BPP after (AOP proxy here) → ready → destroy. @PostConstruct is not advised: proxy does not exist yet. CommonAnnotationBeanPostProcessor runs @PostConstruct in before-init.
