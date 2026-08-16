<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чем разница между `model.put()` и `model.addAttribute()`?**

Метод addAttribute отделяет нас от работы с базовой структурой hashmap. По сути addAttribute это обертка над put, где делается дополнительная проверка на null. Метод addAttribute в отличие от put возвращает modelmap.

````java
model.addAttribute(“attribute1”,”value1”).addAttribute(“attribute2”,”value2”);
````
