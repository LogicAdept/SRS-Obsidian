<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем @RestController отличается от @Controller?**

@RestController = @Controller + @ResponseBody. То есть результаты методов сразу сериализуются в JSON / XML (через Jackson) и отдаются в body ответа. @Controller сам по себе ожидает имя view (для рендера HTML), что для REST не нужно.

**В чём разница между `@Controller` и `@RestController`?**

`@RestController` = `@Controller` + `@ResponseBody`

`@RestController` превращает помеченный класс в Spring-бин. Этот бин для конвертации входящих/исходящих данных
использует Jackson message converter. Как правило целевые данные представлены в json или xml.

**@RestController = ?**

@Controller + @ResponseBody: return JSON/bytes, not a view name. @Controller + ViewResolver for SSR.
