<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Servlet #SRS

# What is the difference between `web.xml` and Spring `servlet.xml`?

> [!abstract] Short answer
> **`WEB-INF/web.xml` is the Jakarta Servlet deployment descriptor**: it tells the **container** about servlets, filters, listeners, mappings, and context params. Interview “servlet.xml” means Spring’s **`/WEB-INF/{servlet-name}-servlet.xml`** — the **default XML for that `DispatcherServlet`’s `WebApplicationContext`**. It is **not** a Servlet-spec file. Root beans default to **`/WEB-INF/applicationContext.xml`** via `ContextLoaderListener`. Today you often have **neither**: Java `WebApplicationInitializer` or Boot.

## Container descriptor vs Spring bean XML

Jakarta tutorial: `web.xml` is optional when annotations suffice; when both exist, the **descriptor wins**. Typical Spring entries: `<listener>` for `ContextLoaderListener`, `<context-param name="contextConfigLocation">` for the **root**, `<servlet>` for `DispatcherServlet` plus `<servlet-mapping>`, and a servlet **init-param** `contextConfigLocation` if you do not want the default child XML.

`XmlWebApplicationContext`: root default **`/WEB-INF/applicationContext.xml`**. A servlet named **`test`** loads **`/WEB-INF/test-servlet.xml`**. Override with `contextConfigLocation` (comma/space-separated paths; later files override beans). Default context class is XML unless you set `contextClass`.

`web.xml` never defines Spring beans. The `*-servlet.xml` never registers the servlet with the container.

```xml
<listener>
  <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<context-param>
  <param-name>contextConfigLocation</param-name>
  <param-value>/WEB-INF/applicationContext.xml</param-value>
</context-param>
<servlet>
  <servlet-name>dispatcher</servlet-name>
  <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
  <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
  <servlet-name>dispatcher</servlet-name>
  <url-pattern>/</url-pattern>
</servlet-mapping>
```

**Listing 1.** Conceptual: with servlet-name `dispatcher`, Spring loads **`/WEB-INF/dispatcher-servlet.xml`** unless you set the servlet’s `contextConfigLocation`. Front controller: [[What is Spring MVC DispatcherServlet]]. Root vs child: [[What is the difference between DispatcherServlet and ContextLoaderListener]]. Java instead of XML: [[What is WebApplicationInitializer in Spring MVC]].

```d2
direction: down
web: "web.xml\ncontainer: servlet, filter, listener" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
root: "/WEB-INF/applicationContext.xml\nroot WebApplicationContext" {
  width: 340
  height: 55
  style.fill: "#fff3e0"
}
child: "/WEB-INF/dispatcher-servlet.xml\nMVC beans" {
  width: 340
  height: 55
  style.fill: "#e8f5e9"
}

web -> root
web -> child
```

**Fig. 1.** `web.xml` boots the container pieces. Spring XML files fill the IoC contexts those pieces start.

> [!warning] There is no standard `servlet.xml`
> The filename is **`{servlet-name}-servlet.xml`**. A file literally named `servlet.xml` is loaded **only** if the servlet-name is `servlet` or you point `contextConfigLocation` at it.

> [!warning] Two files, two contexts
> Controllers in the **child** XML are invisible to a **root-only** lookup. Services in the child are invisible to other servlets. Put shared beans in **`applicationContext.xml`** (or the Java root config).

> [!warning] Boot and Servlet 3 skip both
> Embedded Boot does not use `web.xml`. `AbstractAnnotationConfigDispatcherServletInitializer` registers the servlet in Java. `@EnableWebMvc` / `@Configuration` replace the XML bean files.

> [!tip] Interview answer
> **`web.xml` is the Servlet deployment descriptor.** “servlet.xml” is Spring’s default **`/WEB-INF/<servlet-name>-servlet.xml`** for that `DispatcherServlet`. Root context is **`applicationContext.xml`**. The first talks to the container; the second lists Spring beans.
