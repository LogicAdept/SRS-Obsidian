<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Цепочка запросов в Postman.**

1) POST /auth/login → получить accessToken. 2) В Tests: pm.environment.set("token", jsonData.accessToken). 3) GET /users/me с заголовком Authorization: Bearer {{token}}. 4) Проверка: pm.expect(pm.response.code).to.eql(200). Pre-request Script: генерация timestamp, подпись HMAC- SHA256.
