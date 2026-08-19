<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Common `ApplicationContext` implementations:

- `ClassPathXmlApplicationContext` — XML on the classpath (relative resource)
- `FileSystemXmlApplicationContext` — XML by filesystem path
- `AnnotationConfigApplicationContext` — `@Configuration` / component scan
- Web: `WebApplicationContext` / `XmlWebApplicationContext` / `GenericWebApplicationContext`
- Dumps also name `GenericGroovyApplicationContext` (Groovy or XML)

You can pass several config files. Boot wraps this; standalone code still `new`s one of these and usually `close()`s it.

> [!warning] Unverified traps from the dump
> - `XmlBeanFactory` appears in old lists as the `BeanFactory` impl; it is not the modern default.
> - Classpath vs file-system path is the usual mix-up on the two XML contexts.
