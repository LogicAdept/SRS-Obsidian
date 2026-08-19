<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Stereotypes #Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем @Component отличается от @Service, @Repository, @Controller?**

Технически почти ничем — все они помечают бин для регистрации в контексте. Но семантически: @Service — бизнес-логика, @Repository — работа с БД (плюс перевод исключений в DataAccessException), @Controller — веб-слой.

**Чем @Component отличается от @Service, @Repository, @Controller?**

Технически почти ничем, все регистрируют бин. Семантически: @Service — бизнес-логика, @Repository — работа с БД + перевод исключений в DataAccessException, @Controller — веб-слой. @RestController = @Controller + @ResponseBody.

**Чем отличается @Component, @Service, @Repository, @Controller?**

Технически — все создают бин (синглтон по умолчанию). Семантически разные: @Repository — слой доступа к данным, Spring дополнительно оборачивает SQL/JPA исключения в DataAccessException. @Service — бизнес-логика. @Controller — web-слой. @Component — общий. Использование правильной аннотации улучшает читаемость кода.

**How do @Component, @Service, @Repository, @Controller and @RestController differ?**

Источник: https://habr.com/ru/articles/967632/

@Component — базовая, любой бин. @Service — тот же Component, семантика бизнес-логики. @Repository — DAO, плюс перевод исключений БД в DataAccessException. @Controller — MVC, по умолчанию HTML/шаблоны. @RestController = @Controller + @ResponseBody, по умолчанию JSON.
