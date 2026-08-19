<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что делает Spring Security?**

Защищает приложение: аутентификация (кто ты) и авторизация (что тебе можно). Работает через цепочку фильтров перед твоим контроллером.

**Spring Security 6 in one minute?**

Filter chain in front of MVC. Authentication (who) then authorization (what). Boot 3: SecurityFilterChain bean, not WebSecurityConfigurerAdapter. JWT/OAuth2 resource server vs form login. Method security is extra AOP.
