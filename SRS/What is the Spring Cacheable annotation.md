<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is @Cacheable and why can it fail from @PostConstruct?**

Источник: https://habr.com/ru/articles/967632/

@Cacheable кеширует результат метода по параметрам. Как у транзакций: self-вызов и вызов из @PostConstruct не проходят через прокси.
Для @Cacheable ещё хуже: cache-аспект инициализируется позднее, поэтому вызов из @PostConstruct обычно не работает. Обход: ApplicationRunner/CommandLineRunner + self-injection через @Lazy.

**@Cacheable and proxies again?**

CacheInterceptor AOP. Same self-invocation/@PostConstruct issues as @Transactional. Need @EnableCaching. Key SpEL. Unless/condition. Cache stampede is a follow-up.
