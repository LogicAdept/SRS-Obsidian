<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Cloud, in microservices, is a system that provides integration with external systems. It is a short-lived framework that builds an application, fast. Being associated with the finite amount of data processing, it plays a very important role in microservice architectures.

For typical use cases, Spring Cloud provides the out of the box experiences and a sets of extensive features mentioned below:

* Versioned and distributed configuration.
* Discovery of service registration.
* Service to service calls.
* Routing.
* Circuit breakers and load balancing.
* Cluster state and leadership election.
* Global locks and distributed messaging.

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое Spring Cloud и для чего он?**

Набор инструментов для микросервисов: service discovery (Eureka), конфиг-сервер, API Gateway, Circuit Breaker. На Junior достаточно знать «что это и зачем».

**Spring Cloud pieces that still matter?**

Gateway, Config, OpenFeign/load balancer, CircuitBreaker (Resilience4j), Stream. Netflix OSS (Eureka/Hystrix/Zuul1) is legacy — many interviews still ask the names, answer with replacements.
