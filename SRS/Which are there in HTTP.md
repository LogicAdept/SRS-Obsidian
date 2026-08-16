<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие серии кодов состояния есть в HTTP?**

__Код состояния HTTP (англ. HTTP status code)__ — часть первой строки ответа сервера при запросах по протоколу HTTP. Он представляет собой целое число из трёх десятичных цифр. Первая цифра указывает на класс состояния. За кодом ответа обычно следует отделённая пробелом поясняющая фраза на английском языке, которая разъясняет человеку причину именно такого ответа.

+ __1xx__ (информационные)
    + _100 - Continue_
    + _101 - Switching Protocols_;
    + _102 - Processing_.
+ __2xx__
    + _200 OK_
    + _201 Created_
    + ...
+ __3xx__
    + _300 Multiple Choices_
    + _301 Moved Permanently_
    + _302 Moved Temporarily_
    + _302 Found_
    + ...
+ __4xx__
    + _400 Bad Request_
    + _401 Unauthorized_
    + _402 Payment Required_
    + _403 Forbidden_
    + _404 Not Found_
    + _405 Method Not Allowed_
    + _406 Not Acceptable_
    + _407 Proxy Authentication Required_
    + _408 Request Timeout_
    + ..
+ __5xx__
    + _500 Internal Server Error_
    + _501 Not Implemented_
    + _502 Bad Gateway_
    + _503 Service Unavailable_
    + _504 Gateway Timeout_
    + ...
