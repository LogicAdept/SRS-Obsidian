<!--
reps: 0
priority: 0
-->
#Java/Logging #SRS

# How do you configure logging in a Spring Boot application?

> [!abstract] Short answer
> Starters pull **Logback** (`spring-boot-starter-logging`, transitively via `spring-boot-starter-web`). Default is **console**, levels **ERROR / WARN / INFO**. Set **`logging.level.<logger>`** (and **`logging.level.root`**) in `application.properties`. Add a **file** with **`logging.file.name`** or **`logging.file.path`** (not the old `logging.file`). For Logback XML, prefer **`logback-spring.xml`**. Switch implementation by excluding the logging starter and adding **`spring-boot-starter-log4j2`**. Logging starts **before** the `ApplicationContext`, so `@PropertySource` cannot choose the system.

## Properties first, native file if you need more

Boot’s `LoggingSystem` picks Logback when it is on the classpath. Commons Logging / JUL / Log4J calls are routed. Default output is **console only**.

```properties
logging.level.root=warn
logging.level.org.springframework.web=debug
logging.level.org.hibernate=error
logging.file.name=myapplication.log
logging.pattern.console=%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n
```

**Listing 1.** Levels: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, `OFF`. Logback maps **`FATAL` → `ERROR`**. Env vars work for **packages** (`LOGGING_LEVEL_ORG_SPRINGFRAMEWORK_WEB=DEBUG`), not a single class (relaxed binding lowercases). Groups: built-in **`web`** and **`sql`**, or `logging.group.tomcat=…` then `logging.level.tomcat=trace`. File: **`logging.file.name`** writes that path; **`logging.file.path`** writes **`spring.log`** in that directory; if both are set, **name wins** and path is ignored. Rotation (Logback via properties): `logging.logback.rollingpolicy.*` (default archive **7** files, **10 MB**).

`--debug` / `debug=true` is **not** “everything DEBUG” — it raises a **fixed set of core loggers** (and the conditions report) ([[How can you debug which auto-configuration classes applied]]). `--trace` / `trace=true` is the louder cousin.

```xml
<configuration>
	<include resource="org/springframework/boot/logging/logback/defaults.xml"/>
	<include resource="org/springframework/boot/logging/logback/console-appender.xml"/>
	<root level="INFO">
		<appender-ref ref="CONSOLE"/>
	</root>
	<logger name="org.springframework.web" level="DEBUG"/>
</configuration>
```

**Listing 2.** Native Logback on the classpath (or `logging.config`). Use **`logback-spring.xml`** so Boot extensions work: **`springProfile`**, **`springProperty`**. Plain **`logback.xml`** loads **too early**. Placeholders in logging properties use Boot’s **`:`** default delimiter, not Logback `:-`. Includes: `console-appender.xml`, `file-appender.xml`, structured variants. `${LOG_FILE}` / `${LOG_PATH}` come from `logging.file.name` / `logging.file.path`.

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter</artifactId>
	<exclusions>
		<exclusion>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-logging</artifactId>
		</exclusion>
	</exclusions>
</dependency>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-log4j2</artifactId>
</dependency>
```

**Listing 3.** Official Log4j 2 swap: exclude **`spring-boot-starter-logging`**, add **`spring-boot-starter-log4j2`**. Config files: `log4j2-spring.xml` / `log4j2.xml`. JUL in an executable JAR is discouraged.

Structured JSON without XML: `logging.structured.format.console=ecs` (or `gelf`, `logstash`). Runtime level changes: Actuator **`loggers`** ([[How do you change log levels at runtime with Actuator]]). Profile-specific Logback blocks belong in **`logback-spring.xml`** ([[How do you activate a Spring profile]]).

```d2
direction: down
props: "logging.level.*\nlogging.file.name" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
xml: "logback-spring.xml\n(or log4j2-spring.xml)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
sys: "LoggingSystem\nbefore ApplicationContext" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

props -> sys
xml -> sys
```

**Fig. 1.** Environment properties and the native file both feed `LoggingSystem`. Disable Boot logging entirely with system property **`org.springframework.boot.logging.LoggingSystem=none`**.

> [!warning] `logging.file` is not the current property
> Dumps still show `logging.file=app.log`. Use **`logging.file.name`** or **`logging.file.path`**. `logback.configurationFile` is **not** a Boot-managed key. A custom `logback.xml` that does **not** include Boot’s appenders **drops** console coloring and default patterns unless you re-include `defaults.xml`.

> [!warning] Too early for `@PropertySource`
> Logging is configured **before** the context exists. `@PropertySource` on a `@Configuration` class cannot switch Logback vs Log4j2. WAR deployments skip Boot’s log shutdown hook (`logging.register-shutdown-hook=false` if you need that). `springProfile` in **`logback.xml`** (not `-spring`) fails with “no applicable action”.

> [!tip] Interview answer
> Boot defaults to Logback on the console at INFO. I set logging.level and logging.file.name in application.properties, and I use logback-spring.xml when I need appenders or springProfile. logging.file is the old name. To use Log4j2 I exclude spring-boot-starter-logging and add spring-boot-starter-log4j2. Logging starts before the ApplicationContext, so I do not try to configure it from @PropertySource.
