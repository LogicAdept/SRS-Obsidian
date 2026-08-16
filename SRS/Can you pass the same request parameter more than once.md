<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Можно ли передать в запросе один и тот же параметр несколько раз?**

Пример: `http://localhost:8080/login?name=Ranga&name=Ravi&name=Sathish`
Да, можно принять все значения, используя массив в методе контроллера

````java
public String method(@RequestParam(value="name") String[] names){
}
````
