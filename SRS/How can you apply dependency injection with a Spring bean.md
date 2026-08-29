<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/DI #SRS

# How can you apply dependency injection with a Spring bean?

> [!abstract] Short answer
> Declare the collaborator on the bean; let the container **supply** it when the instance is created. Official DI uses **constructor arguments**, **factory-method arguments**, or **properties after construction** (setters). In practice you write that as XML `<constructor-arg>` / `<property>`, as `@Bean` method **parameters**, or as `@Autowired` / `@Inject` on a **constructor**, **setter**, **field**, or **config method**. Autowiring can also infer the collaborator (`byType` / `byName`, or annotation type-matching). That is **wiring** ([[How would you explain dependency injection]]) — not `new` and not a service locator.

## Write the injection point, then the definition

The IoC chapter’s definition: objects expose dependencies **only** through constructor args, factory-method args, or properties set after construction. The `ApplicationContext` injects them from `BeanDefinition` metadata (XML, stereotypes, `@Bean`).

**Constructor (preferred for required deps).** XML `<constructor-arg ref="…"/>`, or a constructor (single constructor is autowired with no annotation ([[Why is Autowired often omitted on a single constructor in modern Spring]])). Static **factory-method** arguments are treated the same way.

**Setter / config method.** XML `<property name="finder" ref="movieFinder"/>`, or `@Autowired` on `setFinder` **or** on a method with any name and several arguments ([[Can Autowired be applied to methods other than constructors and setters]]). Mix: required collaborators in the constructor, optional ones on setters ([[Which dependency injection styles do you know]]).

**Field.** `@Autowired` / `@Inject` / `@Resource` on a field. Convenient; not `final`; not one of the two “major variants” in the DI chapter.

```java
@Service
public class SimpleMovieLister {

    private final MovieFinder movieFinder;

    public SimpleMovieLister(MovieFinder movieFinder) {
        this.movieFinder = movieFinder;
    }
}

@Configuration
public class MovieConfig {

    @Bean
    MovieFinder movieFinder() { return new JpaMovieFinder(); }
}
```

**Listing 1.** Conceptual. `@Bean` **parameters** are DI too: `movieLister(MovieFinder finder)` would inject the `movieFinder` bean. Component scan + a single constructor does the same without `@Autowired`.

```xml
<bean id="movieFinder" class="example.JpaMovieFinder"/>
<bean id="movieLister" class="example.SimpleMovieLister">
    <constructor-arg ref="movieFinder"/>
</bean>
```

**Listing 2.** Conceptual. Explicit `ref` always overrides XML autowire. Modes `byName` / `byType` / `constructor` infer collaborators ([[What XML autowiring modes exist in Spring]]).

**Lookup** (`@Lookup` / `<lookup-method>`) is DI for a **new** instance per call, not a one-time constructor/setter injection.

Do not `@Autowired` your own `BeanPostProcessor` types; wire those with XML or `@Bean`.

```d2
direction: down
def: "BeanDefinition\n(XML / @Bean / @Component)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
create: "create bean" {
  width: 140
  height: 36
  style.fill: "#fff3e0"
}
inject: "inject ctor / factory / property" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

def -> create
create -> inject
```

**Fig. 1.** Metadata first; injection happens when the bean is created, not when the file is parsed.

> [!warning] Injection point vs lookup
> `applicationContext.getBean(MovieFinder.class)` inside business code is **not** the DI style the docs start from. Prefer constructor/setter/`@Bean` parameters so tests can pass a stub without a container.

> [!warning] Type match with two beans
> Two singletons of the same type are legal; a single-valued `@Autowired MovieFinder` then fails unless you name, `@Primary`, or `@Qualifier` them ([[Can you create two singleton beans of the same type in Spring]]).

> [!tip] Interview answer
> You apply DI by declaring the dependency on the bean — constructor, factory method, setter, field, or config method — and listing the collaborator in XML, as a @Bean parameter, or via autowiring. The container injects when it creates the instance. I use constructors for required collaborators and setters or ObjectProvider for optional ones.
