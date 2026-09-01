<!--
reps: 0
priority: 0
-->
#Java/Testing/Mockito #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ArgumentCaptor.**

Захват аргумента: verify(repo).save(captor.capture()); assertThat(captor.getValue().getName()).isEqualTo("Alice"). Когда нужно проверить не факт вызова, а конкретные значения.

**ArgumentCaptor.**

Захват аргумента, с которым был вызван метод, для последующих проверок. Удобно, когда нужно проверить не просто факт вызова, а что именно передали.

**ArgumentCaptor — зачем нужен?**

Захват аргумента, переданного в замоканный метод. verify(service).send(captor.capture()); assertThat(captor.getValue().getEmail()).isEqualTo("test@mts.ru"). Для AQA: проверить, что сервис отправляет правильные данные во внешний API.
