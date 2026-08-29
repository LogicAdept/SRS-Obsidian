<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# Which ApplicationContext implementations are commonly used?

> [!abstract] Short answer
> Standalone, the docs name **`ClassPathXmlApplicationContext`** and **`FileSystemXmlApplicationContext`**. Java config uses **`AnnotationConfigApplicationContext`** (since **3.0**: `@Configuration`, `@Component`, or `jakarta.inject` types; also `register` / `scan`). The flexible base is **`GenericApplicationContext`** plus a reader (`XmlBeanDefinitionReader`, `GroovyBeanDefinitionReader`). Groovy XML-or-beans: **`GenericGroovyApplicationContext`**. Web code uses a **`WebApplicationContext` implementation** (`XmlWebApplicationContext`, `AnnotationConfigWebApplicationContext`, `GenericWebApplicationContext`) — `WebApplicationContext` itself is an **interface**. Boot **does not** make you `new` these; it picks an annotation-config web or reactive subtype ([[What ApplicationContext type does Spring Boot create for a web app]]).

## Convenience subclasses vs one generic context

The `ApplicationContext` **interface** is what you program to. Concrete types mainly differ by **how configuration is loaded** and **how unprefixed resource paths resolve**.

```java
ApplicationContext xml = new ClassPathXmlApplicationContext("services.xml", "daos.xml");
ApplicationContext java = new AnnotationConfigApplicationContext(AppConfig.class);
```

**Listing 1.** Conceptual. Multiple XML locations: **later files override** earlier bean ids. The `Class<?>…` / `String…` `AnnotationConfigApplicationContext` constructors **refresh immediately**; the no-arg form needs `register`/`scan` then `refresh()`.

| Type | Typical input | Unprefixed path |
| --- | --- | --- |
| `ClassPathXmlApplicationContext` | XML on the classpath (JAR-friendly, tests) | `ClassPathResource` |
| `FileSystemXmlApplicationContext` | XML on disk (cwd-relative even with a leading `/`) | `FileSystemResource` |
| `AnnotationConfigApplicationContext` | Component classes / package scan | Classpath-style loader (extends `GenericApplicationContext`) |
| `GenericGroovyApplicationContext` | `.groovy` (also understands XML) | Groovy-aware |
| `GenericApplicationContext` | You attach readers, then `refresh()` | You choose the `Resource` |

Javadoc calls the XML types a **one-stop convenience**; prefer `GenericApplicationContext` + `XmlBeanDefinitionReader` when you need to configure first, then refresh once ([[What is the difference between close and refresh on ApplicationContext]] — `GenericApplicationContext` does **not** support a second refresh).

Web: `request`/`session`/`application` scopes need a web-aware context, not `ClassPathXmlApplicationContext` ([[What is the difference between ApplicationContext and WebApplicationContext]]). Servlet apps historically use `XmlWebApplicationContext` or `AnnotationConfigWebApplicationContext` (`contextClass` on `ContextLoaderListener` / `DispatcherServlet`).

`XmlBeanFactory` is **not** a current `ApplicationContext`. The usual `BeanFactory` implementation is `DefaultListableBeanFactory` inside these contexts.

```d2
direction: down
iface: "ApplicationContext" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
xml: "ClassPath / FileSystem XML" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
ann: "AnnotationConfig*" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
web: "WebApplicationContext impls" {
  width: 240
  height: 40
  style.fill: "#f3e5f5"
}

iface -> xml
iface -> ann
iface -> web
```

**Fig. 1.** Same interface; pick the implementation that matches metadata format and environment (standalone vs servlet).

> [!warning] Same string, different `Resource`
> `new FileSystemXmlApplicationContext("conf/appContext.xml")` reads the **working directory**. The same string on `ClassPathXmlApplicationContext` reads the **classpath**. A `classpath:` prefix on a `FileSystemXmlApplicationContext` **does** load the file from the classpath, but later unprefixed `getResource` calls are **still** filesystem paths. A leading slash is **not** an absolute disk path for that type.

> [!warning] `WebApplicationContext` is not a class you `new` in a console app
> It is the web **contract**. Instantiating `ClassPathXmlApplicationContext` in a servlet test will not give you request scope. Boot’s servlet/reactive context classes are **Boot** types, not Framework XML contexts.

> [!tip] Interview answer
> For a standalone app you typically new ClassPathXmlApplicationContext or AnnotationConfigApplicationContext; FileSystemXmlApplicationContext is the disk variant and treats plain paths as cwd-relative. GenericApplicationContext plus a reader is the flexible form. In a web app you need a WebApplicationContext implementation, and Boot chooses one for you from the classpath.
