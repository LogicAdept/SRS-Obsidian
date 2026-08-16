<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как сделать REST-эндпоинт?**

Класс с @RestController, метод с @GetMapping/@PostMapping. Параметры — @PathVariable, @RequestParam, @RequestBody. Возвращаемый объект сериализуется в JSON через Jackson.

**Как обработать исключение в REST-контроллере?**

@ExceptionHandler в самом контроллере или глобально через @RestControllerAdvice + @ExceptionHandler.

**Как сделать REST-эндпоинт?**

Класс с @RestController, метод с @GetMapping/@PostMapping. Параметры — @PathVariable, @RequestParam, @RequestBody. Возвращаемый объект сериализуется в JSON через Jackson.

**Какие принципы у REST?**

Stateless — сервер не хранит сессию клиента, каждый запрос самодостаточен. Cacheable — ответы могут кэшироваться. Uniform interface — единый интерфейс через HTTP-методы и URL. Layered system — между клиентом и сервером могут быть прокси, балансеры. Client-Server — клиент и сервер независимы. HATEOAS — клиент находит переходы через ссылки в ответах (на практике редко делают).
