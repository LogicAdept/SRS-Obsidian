<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/Spring/Boot #SRS

# What does a typical Java web application project structure look like?

> [!abstract] Short answer
> **Build** (Maven): `pom.xml`, `src/main/java`, `src/main/resources`, **`src/main/webapp`** (static files + **`WEB-INF/web.xml`**), `src/test/java`. **Runtime WAR** (Servlet): document root + **`WEB-INF/`** (`web.xml`, **`classes/`**, **`lib/*.jar`**). **`WEB-INF` is not public** (404). Spring Boot often **omits** `webapp/` and uses a **root-package** `MyApplication` plus classpath resources; the default artifact is an **executable JAR** (`BOOT-INF/`), not a WAR.

## Source tree vs packaged WAR

Maven’s standard layout is the usual **project** shape. The WAR plugin maps `src/main/java` + `resources` into **`WEB-INF/classes`**, and `src/main/webapp` into the archive **root**.

```text
pom.xml
src/main/java/.../SampleAction.java
src/main/resources/images/sampleimage.jpg
src/main/webapp/WEB-INF/web.xml
src/main/webapp/index.jsp
src/test/java/
target/          (build output only)
```

**Listing 1.** Maven WAR project (official WAR plugin sample). `src` and `target` at the top; Java packages under `src/main/java`. Servlet **3+** can skip `web.xml` if you use annotations / `ServletContainerInitializer`; the **directory** is still the contract.

Packaged application (Servlet spec **§10.5**):

```text
/index.html
/howto.jsp
/images/banner.gif
/WEB-INF/web.xml
/WEB-INF/classes/com/mycorp/servlets/MyServlet.class
/WEB-INF/lib/catalog.jar
```

**Listing 2.** Document root is public. **`WEB-INF/classes`** then **`WEB-INF/lib`** on the web app class loader. `META-INF/` in the WAR is also **not** served (404). Static files inside `WEB-INF/lib/*.jar` → `META-INF/resources/` **are** servable, after the real document root.

Spring Boot **does not require** this `webapp/` tree. Recommended **code** layout: `MyApplication` in a **root** package (`com.example.myapplication`) with `customer` / `order` underneath so `@SpringBootApplication` scan and JPA entity scan see the whole app ([[Why should the SpringBootApplication class sit in the root package]], [[What is @SpringBootApplication]]). `application.properties` / YAML live under `src/main/resources`. Default packaging is **`java -jar`** with **`BOOT-INF/classes`** and **`BOOT-INF/lib`**. A WAR for an **external** Tomcat still uses **`WEB-INF/`** plus `SpringBootServletInitializer` ([[How do you deploy a Spring Boot application as a WAR]], [[What is an executable JAR in Spring Boot]]).

```d2
direction: down
src: "Maven src/main\njava + resources + webapp" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
war: "WAR / servlet container\nWEB-INF/classes + lib" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
boot: "Boot JAR (typical)\nBOOT-INF + embedded server" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

src -> war
src -> boot
```

**Fig. 1.** Same Java sources; two packaging stories. IoC (`ApplicationContext`) is **inside** the web app, not a folder next to `WEB-INF` ([[How does a Spring IoC container differ from a web container or EJB container]]).

> [!warning] `WEB-INF` is not a source folder you browse in the browser
> Clients requesting `/WEB-INF/...` get **404**. Classes belong in `src/main/java`, not under `webapp/WEB-INF/classes` in source (the plugin puts them there at package time). Do not commit `target/`.

> [!warning] Boot is not `src/main/webapp` or bust
> A Boot web app can be **only** `src/main/java` + `src/main/resources` (Thymeleaf/static on the classpath: `static/`, `templates/`). Requiring `web.xml` and JSPs is the **classic WAR** interview answer, not the Boot default.

> [!tip] Interview answer
> I describe Maven src/main/java, resources, and webapp with WEB-INF, then the WAR shape: public root, WEB-INF/classes, WEB-INF/lib. For Spring Boot I put the main class in the root package and usually ship an executable JAR; a WAR is only when an external servlet container must own the app.
