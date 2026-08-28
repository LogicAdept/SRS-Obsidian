<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS

# What is `@ContextHierarchy`?

> [!abstract] Short answer
> **`@ContextHierarchy`** (Spring Framework 3.2.2+) on a test class lists **one or more `@ContextConfiguration` levels**, loaded as a **parent–child `ApplicationContext` tree**. Typical picture: root (shared services) plus a **child** (MVC `DispatcherServlet` config, a Batch job). The context **autowired into the test** is the **lowest / child** context.

## Why a tree, not one context

A Spring MVC app often has a root `WebApplicationContext` (`ContextLoaderListener`) and a child (`DispatcherServlet`). Batch jobs similarly nest job config under shared infrastructure. Tests mirror that with `@ContextHierarchy({ @ContextConfiguration(...), @ContextConfiguration(...) })`, usually plus `@WebAppConfiguration` for web.

```java
@ExtendWith(SpringExtension.class)
@WebAppConfiguration
@ContextHierarchy({
	@ContextConfiguration(classes = TestAppConfig.class),
	@ContextConfiguration(classes = WebConfig.class)
})
class ControllerIntegrationTests {

	@Autowired
	WebApplicationContext wac;
}
```

**Listing 1.** Conceptual: `wac` is the **child** (WebConfig), whose parent is TestAppConfig. Engine: [[What is the Spring TestContext Framework]]. Each level is [[What is the ContextConfiguration annotation]].

A superclass can declare a single `@ContextConfiguration` **without** `@ContextHierarchy`. Subclasses that then use `@ContextHierarchy` get that superclass context as **parent** of their child level (implicit parent).

## Named levels: merge vs override

To **merge** or **override** a level across a test class hierarchy, set the same **`name`** on `@ContextConfiguration` at each corresponding level. Merging a named level requires the **same resource type** (all XML or all component classes) at that level. Different levels in one hierarchy may mix XML and classes.

- Same `name`, default **`inheritLocations = true`**: locations/classes are **appended** (child cache key is the merged list; parent level is still shared).
- Same `name`, **`inheritLocations = false`**: that level is **replaced**; parent of the new child is still the named parent context.

As of Framework **6.2.6**, `name` also targets bean overrides: `@MockitoBean(contextName = "child")`. **`@Autowired` always injects from the lowest context**; to hold mocks from **parent and child**, inject the override fields themselves (`@MockitoBean(contextName = "parent")` vs `"child"`).

```d2
direction: down
root: "parent level\n(TestAppConfig / app-config.xml)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
child: "child level\n(WebConfig / servlet XML)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
test: "@Autowired WAC / beans\n= child context" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}

root -> child
child -> test
```

**Fig. 1.** Beans in the parent are visible to the child. The test’s autowired `ApplicationContext` is the child.

> [!warning]Unnamed levels do not merge
> Without a matching **`name`**, a subclass `@ContextHierarchy` does **not** merge a superclass level. You get extra contexts or surprising parents. Mixing XML and `@Configuration` **on the same named level** when merging is invalid.

> [!warning]DirtiesContext default is exhaustive
> [[What is DirtiesContext]] `hierarchyMode` defaults to **`EXHAUSTIVE`**: closing the child also evicts **other cached hierarchies that share an ancestor**. Use **`CURRENT_LEVEL`** when only the child is dirty. Cache keys include the **parent** configuration — [[How does the Spring TestContext framework cache the ApplicationContext]].

> [!tip] Interview answer
> **`@ContextHierarchy` stacks `@ContextConfiguration` entries into a parent–child context tree**, the test analogue of root WAC plus servlet WAC. The test injects the **child**. Name levels to merge or override in subclasses; `@Autowired` will not give you the parent context. Dirtying a hierarchy is exhaustive unless you set `CURRENT_LEVEL`.
