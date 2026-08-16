<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**How do BeanFactoryPostProcessor and BeanPostProcessor differ?**

Источник: https://habr.com/ru/articles/967632/

BeanFactoryPostProcessor меняет метаданные бинов до их создания. Пример: PropertySourcesPlaceholderConfigurer.
BeanPostProcessor работает с уже созданным бином (прокси, AOP, @Transactional).
