<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Spring/Framework/WebMvc #SRS

# How many Spring application contexts can an application have?

> [!abstract] Short answer
> **As many as you create** — there is **no** “one context per JVM” rule. A process may hold **several independent** `ApplicationContext`s, or a **parent–child tree** (`HierarchicalBeanFactory`). Classic Spring MVC often has **one root** plus **one child per `DispatcherServlet`** (any number of those servlets). Many apps use a **single** `WebApplicationContext`; **Spring Boot** typically starts **one** context unless you build a hierarchy with `SpringApplicationBuilder`. Child beans **override** the parent; lookup walks **up**. Post-processors and `annotation-config` apply **only in the context where they are defined**.

## One, two, or a tree

`ApplicationContext` extra capabilities include **loading multiple (hierarchical) contexts** so each layer (for example the web layer) has its own factory. `getParent()` is `null` for a root. `setParent` merges a `ConfigurableEnvironment` from the parent into the child.

```d2
JVM: {
  Root: "root WebApplicationContext\nservices, DataSource"
  App1: "DispatcherServlet app1\ncontrollers, HandlerMapping"
  App2: "DispatcherServlet app2"
  Other: "unrelated AnnotationConfigApplicationContext\n(no parent)"
  Root -> App1: parent
  Root -> App2: parent
}
```

**Fig. 1.** Hierarchy is optional. Two `new` contexts without `setParent` are **two islands**, not “the” application context twice.

**Standalone / Boot default:** one context after `SpringApplication.run` / `new AnnotationConfigApplicationContext(...)` ([[Which ApplicationContext implementations are commonly used]], [[What ApplicationContext type does Spring Boot create for a web app]]).

**Servlet MVC:** `DispatcherServlet` **expects** a `WebApplicationContext`. Docs: **a single** one is “simple and sufficient.” **Or** a **root** shared across servlets (`ContextLoaderListener`) and a **child** per servlet. `DispatcherServlet` javadoc: a web app can define **any number** of dispatcher servlets; each loads **its own** context; only the **root** (if any) is shared ([[What is a WebApplicationContext in Spring MVC]]).

```java
public class MyWebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

	@Override
	protected Class<?>[] getRootConfigClasses() {
		return new Class[] { RootConfig.class };
	}

	@Override
	protected Class<?>[] getServletConfigClasses() {
		return new Class[] { App1Config.class };
	}

	@Override
	protected String[] getServletMappings() {
		return new String[] { "/app1/*" };
	}
}
```

**Listing 1.** Official split: root config vs servlet config — **two** contexts in one WAR, not a hard maximum.

**Boot hierarchy:** `SpringApplicationBuilder.parent(...).child(...)`. Restriction: **web components belong in the child**; parent and child share the **same `Environment`**. Events published in a child are also delivered to **ancestor** listeners (same event type may be seen more than once).

**Tests:** `@ContextHierarchy` models the same tree ([[What is ContextHierarchy]]).

## What “another context” actually means

Each context has its **own** singleton cache, post-processors, and (for `ApplicationContext`) event multicaster. A `BeanPostProcessor` in the child does **not** process parent beans. `context:annotation-config` in the **servlet** context autowires **controllers there**, not services that live only in the **root** — that is why services go in the parent.

Same bean **name** in the child **hides** the parent definition for lookups from the child. `containsLocalBean` tells you whether the name is **local**.

> [!warning] “Always two contexts” is a Boot-era myth
> Interviews recite root + `DispatcherServlet` because of WAR + `ContextLoaderListener`. Boot’s embedded servlet path often **is** one `ServletWebServerApplicationContext`. Inventing a second context without a parent link does not share beans.

> [!tip] Interview answer
> Unlimited in principle. Typical: **one** (Boot/simple MVC) or **root + N servlet children**. They compose through **parent**, not through a global singleton. Isolate layers; do not assume every `getBean` sees every bean in the JVM.
