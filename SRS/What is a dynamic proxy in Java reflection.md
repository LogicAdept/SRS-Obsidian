<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS

# What is a dynamic proxy in Java reflection?

> [!abstract] Short answer
> **A runtime-generated class from `java.lang.reflect.Proxy` that implements given interfaces and forwards every interface call to an `InvocationHandler`.** Create it with `Proxy.newProxyInstance(loader, interfaces, handler)`. The result is an instance of a **final** subclass of `Proxy`. It is **interface-only**: you cannot pass a concrete class. Since 1.3.

## `newProxyInstance`, then `invoke`

`Proxy` “provides static methods for creating objects that act like instances of interfaces but allow for customized method invocation.” A **proxy class** is generated at runtime for a list of **proxy interfaces**. A **proxy instance** of that class holds one `InvocationHandler`. A call through those interfaces is encoded as `handler.invoke(proxy, method, args)` and whatever `invoke` returns is the call’s result ([[How can you invoke a method using reflection]], [[What are some use cases of Java reflection]]).

```d2
direction: down
client: "Caller typed as Foo" {
  width: 220
  height: 45
}
px: "Proxy instance\n(final, extends Proxy, implements Foo)" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
ih: "InvocationHandler.invoke\n(proxy, Method, args)" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
client -> px
px -> ih
```

**Fig. 1.** The generated type stands in for the interfaces. Dispatch is always the handler, not a superclass implementation.

A proxy class is **final** and **non-abstract**, extends `java.lang.reflect.Proxy`, and implements **exactly** the interfaces given, in that order (`getInterfaces` returns them). `proxy instanceof Foo` is true and `(Foo) proxy` succeeds. `Proxy.isProxyClass(cl)` tests the generated class (not merely `Proxy.class.isAssignableFrom`). `Proxy.getInvocationHandler(proxy)` returns the handler; a non-proxy argument is `IllegalArgumentException`.

`equals`, `hashCode`, and `toString` from `Object` are also dispatched to `invoke` (`Method`’s declaring class is `Object`). Other public `Object` methods are **not** overridden. A default method on a proxy interface still hits `invoke`; the handler may call `InvocationHandler.invokeDefault(proxy, method, args)` (since 16) to run `X.super.m(...)`.

```java
interface Foo {
    String greet(String name);
}

class TracingHandler implements InvocationHandler {
    public Object invoke(Object proxy, Method method, Object[] args) {
        return "hello, " + args[0];
    }
}

class Make {
    static Foo foo() {
        return (Foo) Proxy.newProxyInstance(
                Foo.class.getClassLoader(),
                new Class<?>[] { Foo.class },
                new TracingHandler());
    }
}
```

**Listing 1.** JavaDoc shape: loader, interface array, handler. `invoke` receives wrapped primitive args (or `null` when there are none). A primitive return must come back boxed; `null` for a primitive return → `NullPointerException` on the proxy call; a wrong wrapper → `ClassCastException`.

`IllegalArgumentException` if an element is not a **non-hidden, non-sealed interface** (no classes, no primitives), if the same `Class` appears twice, if an interface or a type in a public method signature is not visible through the loader (`Class.forName(name, false, cl) == i`), if non-public interfaces are not all in the **same** package and module, or if duplicate signatures have incompatible returns. Interface **order** matters: the same set in a different order is a different proxy class. Duplicate methods pass the `Method` from the **foremost** interface in that list. `getProxyClass` is **deprecated**; named-module proxy classes are encapsulated, so `Constructor.newInstance` can throw `IllegalAccessException` — use `newProxyInstance`.

A checked exception from `invoke` that is not declared on the interface method (in **all** interfaces that share the signature) becomes `UndeclaredThrowableException`. Spring AOP’s **JDK dynamic proxy** is this API when the bean has an interface; **CGLIB** is a subclass of a concrete class and is not `java.lang.reflect.Proxy` ([[What is an AOP proxy in Spring]], [[What are Spring AOP proxy limitations]]).

> [!warning] Not a stand-in for a class
> `newProxyInstance` rejects classes. There is no JDK `Proxy` for “subclass this service and override methods.” That is a different generator (CGLIB / Byte Buddy). Passing `MyService.class` where `MyService` is a class is `IllegalArgumentException`.

> [!warning] `invoke` is the whole type
> Default methods, `equals` / `hashCode` / `toString`, and interface methods all arrive at the same `invoke`. Returning `null` from a `boolean equals` is an NPE on the caller. Hidden and sealed interfaces cannot be proxied (Java SE 21).

> [!tip] Interview answer
> **`Proxy.newProxyInstance` builds a final class at runtime that implements the interfaces you pass and routes every call to `InvocationHandler.invoke`.** It cannot proxy a concrete class — that is why Spring falls back to CGLIB when there is no interface. **`equals` / `hashCode` / `toString` go through the handler too; a checked exception that the interface does not declare becomes `UndeclaredThrowableException`.**
