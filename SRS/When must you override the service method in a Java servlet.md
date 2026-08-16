<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие действия необходимо проделать при создании сервлетов?**

Чтобы создать сервлет `ExampleServlet`, необходимо описать его в дескрипторе развёртывания:

```xml
<servlet-mapping>
    <servlet-name>ExampleServlet</servlet-name>
    <url-pattern>/example</url-pattern>
</servlet-mapping>
<servlet>
    <servlet-name>ExampleServlet</servlet-name>
    <servlet-class>xyz.company.ExampleServlet</servlet-class>
    <init-param>
        <param-name>config</param-name>
        <param-value>default</param-value>
    </init-param>
</servlet>
```

Затем создать класс `xyz.company.ExampleServlet` путём наследования от `HttpServlet` и реализовать логику его работы в методе `service()` или методах `doGet()`/`doPost()`.
