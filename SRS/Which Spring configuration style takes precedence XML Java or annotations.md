<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# Which Spring configuration style takes precedence: XML, Java, or annotations?

> [!abstract] Short answer
> **None of them ranks the others as a format.** Mix is first-class. **Two different contests:** (1) **Same property, annotation injection vs XML** — annotation injection **runs first**, then XML **property** injection; **XML wins** that property. (2) **Same bean name, two definitions** — there is **no** “XML beats `@Bean`” rule. The **later** registration **replaces** the earlier if `DefaultListableBeanFactory.allowBeanDefinitionOverriding` is **true** (Framework **default `true`**); if **false**, **`BeanDefinitionOverrideException`**. Boot’s `spring.main.allow-bean-definition-overriding` defaults to **`false`**. Special case: a **`@Bean` method silently replaces a scanned component** with the **same name** when the **return type matches** — the factory method is used, not the class constructor ([[What configuration styles exist in Spring]], [[What is the difference between a Spring bean id and a bean alias]]).

## Wiring a property vs registering a name

Interview “precedence” dumps treat **XML / Java `@Configuration` / `@Autowired` / `@Component` scan** as one ladder. They are **not** ([[Which Spring configuration style do you prefer XML Java or annotations and why]]).

**Property (same bean, same setter/field).** Official annotation-config note: **annotation injection before XML injection** → XML **overrides** values wired both ways. Constructor injection already ran; a later XML `<property>` can still set **another** property on that instance ([[What does context annotation-config register]]).

```xml
<bean id="movieLister" class="example.SimpleMovieLister">
	<property name="movieFinder" ref="xmlFinder"/>
</bean>
```

```java
public class SimpleMovieLister {
	@Autowired
	public void setMovieFinder(MovieFinder annotationFinder) { /* … */ }
}
```

**Listing 1.** Conceptual. `annotation-config` injects `annotationFinder` first; XML then sets `movieFinder` to `xmlFinder`. Pick **one** story per dependency.

**Definition (same id, two recipes).** XML `<bean id="x">`, `@Bean x()`, and a scanned `@Service` named `x` are **three ways to register** `x`. Override = **replace the `BeanDefinition`**, not “annotations lose.” Load **order** (which reader/`@ImportResource`/scan ran last) decides **which** recipe remains when overriding is allowed. **`@Bean` vs scan:** if names collide and the method’s return type matches the component class, the container **calls the `@Bean` method** instead of constructing the stereotyped class ([[What is the Spring Bean annotation]]).

```d2
direction: down
wire: "same property\n@Autowired then XML → XML wins" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
def: "same bean name\nlater definition / @Bean vs scan" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}

wire -> def: "different questions"
```

**Fig. 1.** Do not answer with a single ranking. Java-centric `@ImportResource` and XML-centric `<bean class="…Config">` only choose **bootstrap**; they do not invent a third precedence table ([[When is Java configuration more convenient than XML configuration in Spring]]).

> [!warning] “XML always wins” is only the property note
> It does **not** mean XML definitions beat `@Bean` or scan. Two `<bean id="dataSource">` vs `@Bean DataSource dataSource()` is **overriding** (or an exception), not the annotation-config sentence.

> [!warning] Three features share “annotations”
> `@Autowired` (wiring), `@Component` scan (register **this** class), and `@Bean` (factory method) do not have one precedence. `@Autowired` **never** registers a bean ([[When is Java configuration preferable to annotation-based configuration]]).

> [!tip] Interview answer
> There is no overall winner among XML, Java config, and annotations. For the same property, annotation injection runs first and XML overrides it. For the same bean name, a later definition replaces an earlier one if overriding is allowed — Boot turns that off by default. A @Bean method can replace a scanned component with the same name when the return type matches. I keep one bootstrap and one wiring style per dependency so I am not debugging override order.
