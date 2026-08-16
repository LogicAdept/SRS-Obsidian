<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Boot Actuator module use to monitor and manage Spring Boot application by providing production-ready features like health check-up, auditing, metrics gathering, HTTP tracing etc. All of these features can be accessed over JMX or HTTP endpoints.

**Adding Spring Boot Actuator**
```xml
<dependencies>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-actuator</artifactId>
	</dependency>
</dependencies>
```

**Monitoring**: Actuator creates several so-called **endpoints** that can be exposed over HTTP or JMX to let you monitor and interact with application.

For example, There is a `/health` endpoint that provides basic information about the application's health. The `/metrics` endpoint shows several useful metrics information like JVM memory used, system CPU usage, open files, and much more. The `/loggers` endpoint shows application's logs and also lets you change the log level at runtime.
```
http://localhost:8080/actuator

----
{
  "_links": {
    "self": {
      "href": "http://localhost:8080/actuator",
      "templated": false
    },
    "health": {
      "href": "http://localhost:8080/actuator/health",
      "templated": false
    },
    "info": {
      "href": "http://localhost:8080/actuator/info",
      "templated": false
    }
  }
}
```

|Endpoint |Description |
|------------------------|------------------------------------| 
|health | Application health info |
|info | Info about the application |
|env | Properties from environment |
|metrics | Various metrics about the app |
|mappings | @RequestMapping Controller mappings|
|shutdown | Triggers application shutdown |
|httptrace | HTTP request/response log |
|loggers | Display and configure logger info |
|logfile | Contents of the log file |
|threaddump | Perform thread dump |
|heapdump | Obtain JVM heap dump |
|caches | Check available caches |
|integrationgraph | Graph of Spring Integration components|

**Enabling / Disabling endpoints**
```
# Disable an endpoint
management.endpoint.[endpoint-name].enabled=false

# Specific example for 'health' endpoint
management.endpoint.health.enabled=false

# Instead of enabled by default, you can change to mode
# where endpoints need to be explicitly enabled
management.endpoints.enabled-by-default=false
```

**Actuator production checklist?**

health/liveness/readiness, metrics/prometheus, don't expose env/heapdump. Separate management port. Secure endpoints. Custom HealthIndicator.
