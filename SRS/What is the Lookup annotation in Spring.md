<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #Java/Annotations #SRS

# What is the Lookup annotation in Spring?

> [!abstract] Short answer
> `@Lookup` (since **4.1**) is **lookup method injection**: the container **CGLIB-subclasses** your bean and **overrides** a stub or `abstract` method so each call is a `BeanFactory.getBean` for another bean — typically a **prototype**, so a **singleton** can obtain a **new** instance per call. Constructor or setter injection of a prototype happens **once**, when the singleton is created ([[How does a prototype Spring bean behave when injected into a singleton]]). XML is `<lookup-method name="…" bean="…"/>`. It does **not** work on instances returned from `@Bean` factory methods; use `ObjectProvider` / `Provider` there instead.

## Override `getBean`, without `ApplicationContextAware`

Signature of the method to inject: `public` or `protected`, optionally `abstract`, return type of the collaborator. The reference’s classic form is **no arguments**. If you do declare arguments, they are passed through to `getBean` as constructor or factory-method arguments.

`@Lookup("myCommand")` looks up by **name**. Bare `@Lookup` resolves by the method’s **return type**.

```java
@Component
@Scope("prototype")
class AsyncCommand implements Command { /* stateful */ }

@Component
public abstract class CommandManager {

    public Object process(Object commandState) {
        Command command = createCommand();
        command.setState(commandState);
        return command.execute();
    }

    @Lookup
    protected abstract Command createCommand();
}
```

**Listing 1.** Conceptual. Each `createCommand()` is a new prototype if `Command` is prototype-scoped. If the target is a **singleton**, you get the **same** instance every call.

A **concrete** stub (`return null;`) is equally valid: CGLIB replaces the body. That is what component scanning needs (a concrete class). The containing class and the lookup method must **not** be `final` (or `private`).

```xml
<bean id="myCommand" class="example.AsyncCommand" scope="prototype"/>
<bean id="commandManager" class="example.CommandManager">
    <lookup-method name="createCommand" bean="myCommand"/>
</bean>
```

**Listing 2.** Conceptual. Same runtime arrangement as `@Lookup`.

`@Bean` methods in `@Configuration` create the instance themselves; the container **cannot** subclass that object, so `@Lookup` on a type produced that way is a no-op. Inject `ObjectProvider<Command>` (or `Provider`) and call `getObject()` / `get()` per use ([[What is ObjectProvider and a scoped proxy in Spring]]). Scoped proxies are another way to re-resolve a shorter-lived bean.

```d2
direction: down
single: "Singleton CommandManager\n(CGLIB subclass)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
call: "createCommand() each time" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
proto: "new prototype Command" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}

single -> call
call -> proto
```

**Fig. 1.** Lookup runs on each method call, not when the singleton is first wired.

> [!warning] Not `private`, not `final`, not a `@Bean` instance
> CGLIB must subclass the **container-constructed** class. A `final` class/method, a `private` method, or a bean returned from `@Bean` will not be overridden. Tests of an `abstract` host class need your own stub subclass.

> [!warning] Prototype scope is your job
> `@Lookup` only redirects to `getBean`. A singleton target stays a singleton. Forgetting `scope = prototype` (or `@Scope("prototype")`) is the usual “I still get one Command” bug.

> [!tip] Interview answer
> Lookup is method injection: Spring subclasses the singleton and overrides a stub or abstract method so each call getBean’s another bean, usually a prototype. That avoids injecting one prototype for the life of the singleton. It needs a non-final class the container constructs — not a @Bean factory method — and ObjectProvider is the usual alternative.
