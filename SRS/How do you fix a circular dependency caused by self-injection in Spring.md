<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is self-injection in Spring?**

Источник: https://habr.com/ru/articles/967632/

Класс внедряет сам себя через контейнер (обычно прокси), чтобы вызов собственного @Transactional/@Async прошёл через прокси. Прямой this не проходит через прокси.
Типично: @Autowired @Lazy private OrderService self; затем self.processOrder().
