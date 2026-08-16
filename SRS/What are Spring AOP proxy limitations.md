<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What are Spring AOP proxy limitations?**

Источник: https://habr.com/ru/articles/967632/

Вызовы внутри одного класса обходят прокси. Final классы/методы: CGLIB не переопределит final, JDK-прокси только интерфейсы. Private-методы не аопятся — прокси видит public/protected/package-private.
CGLIB — прокси через наследование, если бин не реализует интерфейс (JDK Dynamic Proxy работает только с интерфейсами).

**JDK vs CGLIB and final methods?**

Interface → JDK proxy; otherwise CGLIB subclass. final class: cannot CGLIB. final method: proxy exists but that method is not advised — silent. private not advised. Only method execution join points.
