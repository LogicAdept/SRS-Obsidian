<!--
reps: 0
priority: 0
-->
#API/REST #API/SOAP #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

SOAP (Simple Object Access Protocol) and REST (Representational State Transfer) are both web service communication protocols.
In addition to using HTTP for simplicity, REST offers a number of other benefits over SOAP:

**SOAP**

* SOAP is a protocol.
* SOAP stands for Simple Object Access Protocol.
* SOAP can't use REST because it is a protocol.
* SOAP uses services interfaces to expose the business logic.
* SOAP defines standards to be strictly followed.
* SOAP requires more bandwidth and resource than REST.
* SOAP defines its own security.
* SOAP permits XML data format only.
* SOAP is less preferred than REST.

**REST**

* REST is an architectural style.
* REST stands for Representational State Transfer.
* REST can use SOAP web services because it is a concept and can use any protocol like HTTP, SOAP.
* REST uses URI to expose business logic.
* REST does not define too much standards like SOAP.
* REST requires less bandwidth and resource than SOAP.
* RESTful web services inherits security measures from the underlying transport.
* REST permits different data format such as Plain text, HTML, XML, JSON etc.
* REST more preferred than SOAP.

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**REST vs SOAP.**

REST: HTTP, JSON, легковесный, stateless, гибкий. SOAP: XML, WSDL, строгий контракт, WS- Security. В банках: REST для новых API, SOAP для legacy (АБС, процессинг). Junior AQA: REST — основной, но упомянуть знание SOAP — плюс.

**В чём разница REST и SOAP?**

REST — архитектурный стиль на HTTP. Обычно JSON. Гибкий, контракт через OpenAPI. SOAP — протокол на XML с собственным envelope (Header + Body). Строгий контракт через WSDL. Поддерживает WS-Security (подпись XML, шифрование). В банках живёт в legacy-интеграциях (с ЦБ, межбанком, SWIFT).
