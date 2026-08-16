<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Почему иногда мы используем `@ResponseBody`, а иногда `ResponseEntity`?**

ResponseEntity необходим, только если мы хотим кастомизировать ответ, добавив к нему статус ответа. Во всех остальных случаях будем использовать `@ResponseBody`.

````java
@GetMapping(value=”/resource”)
@ResponseBody
public Resource sayHello() { return resource; }

@PostMapping(value=”/resource”)
public ResponseEntity createResource() {
    ….
    return ResponseEntity.created(resource).build();
}
````

Стандартные HTTP коды статусов ответов, которые можно использовать.
200 — SUCCESS
201 — CREATED
404 — RESOURCE NOT FOUND
400 — BAD REQUEST
401 — UNAUTHORIZED
500 — SERVER ERROR

Для `@ResponseBody` единственные состояния статуса это SUCCESS(200), если всё хорошо и SERVER ERROR(500), если произошла какая-либо ошибка.

Допустим мы что-то создали и хотим отправить статус CREATED(201). В этом случае мы используем `ResponseEntity`.
