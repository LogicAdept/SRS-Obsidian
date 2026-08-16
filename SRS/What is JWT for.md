<!--
reps: 0
priority: 0
-->
#Security/JWT #API #Security/Authentication #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое JWT?**

JSON Web Token — компактный формат для передачи информации в виде подписанного JSON. Состоит из трёх частей через точку: header.payload.signature. Можно проверять валидность без обращения к серверу.

**JWT — структура и как работает?**

Три части через точку: header.payload.signature. Header: алгоритм (HS256). Payload: данные (userId, exp, roles). Signature: HMAC(header+payload, secret). Хранится на клиенте (localStorage/cookie). Проверяется сервером без БД (stateless). exp — время жизни, после которого нужен refresh token.

**JWT in Spring interviews?**

Three Base64 parts: header, claims, signature. Stateless, hard to revoke. Prefer resource-server validation over a home-rolled parser when you have an issuer.
