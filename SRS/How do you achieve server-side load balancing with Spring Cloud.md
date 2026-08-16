<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Server side load balancing can be achieved using `Netflix Zuul`. Zuul is a JVM based router and server side load balancer by Netflix. It provides a single entry to our system, which allows a browser, mobile app, or other user interface to consume services from multiple hosts without managing cross-origin resource sharing (CORS) and authentication for each one. We can integrate Zuul with other Netflix projects like Hystrix for fault tolerance and Eureka for service discovery, or use it to manage routing rules, filters, and load balancing across your system.

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Client-side Load Balancer.**

Round-robin → retry → circuit breaker. Обсудить: health checks, backoff, fallback. Реальная задача Middle в Путешествиях.

**Ribbon is gone — what instead?**

Spring Cloud LoadBalancer (not Ribbon). With OpenFeign or RestClient/WebClient + @LoadBalanced. In k8s, Service DNS often replaces client-side LB.
