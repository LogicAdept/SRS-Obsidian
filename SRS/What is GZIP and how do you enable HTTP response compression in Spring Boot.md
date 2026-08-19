<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Networking/Web #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

GZip compression is a very simple and effective way to save bandwidth and improve the speed of website. It reduces the response time of website by compressing the resources and then sending it over to the clients. It saves bandwidth by at least 50%.

GZip compression is disabled by default in Spring Boot. To enable it, add the following properties to your `application.properties` file
```
# Enable response compression
server.compression.enabled=true

# The comma-separated list of mime types that should be compressed
server.compression.mime-types=text/html,text/xml,text/plain,text/css,text/javascript,application/json

# Compress the response only if the response size is at least 1KB
server.compression.min-response-size=1024
```
