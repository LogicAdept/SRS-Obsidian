<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Boot includes support for embedded Tomcat, Jetty, and Undertow servers. By default the embedded server will listen for HTTP requests on port 8080.

**JAR** 

You can run independently every appliction with different ports (in linux, **java -jar ... > app_logs.log &**) and you can route it (e.g. nginx). Note that, restarting is not problem. You can write custom bash script (like this: **ps aux | grep appname** and kill by PID). But there are some problems with configuring production app. Property files will archived into jar.

**WAR** 

You can deploy into container and just run it. Easy managing at the server. If you want to re-configure app, open properties file from unarchived folder inside container, change it as need and restart container. So, managing and configuring will be easy. But, if you want to run another app in this server with another port, then you must install another copy of container and config it.
