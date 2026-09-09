<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What bean scopes does Quarkus support?

> [!abstract] Short answer
> ArC supports the CDI scopes you actually use in services: **normal scopes** — `@ApplicationScoped` and `@RequestScoped` — where injection hands you a **client proxy** and instantiation is lazy; and **pseudo-scopes** — `@Dependent` (the default) and `@Singleton` — where the instance is created at injection time. `@SessionScoped` exists only with a servlet-capable extension, and Quarkus adds its own scopes (for example `@TransactionScoped`, Vert.x `@LocationScoped`). There is no Spring-style prototype/singleton split — map them to `@Dependent` and `@ApplicationScoped`.

## Normal scopes, proxies, lazy instantiation

A normal-scoped bean is accessed through a client proxy: injecting `@ApplicationScoped Foo` does not construct `Foo`; the first **method invocation** on the proxy resolves the current contextual instance and delegates ([[What is ArC in Quarkus]]). That is why field access on an injected normal-scoped bean is a bug — the proxy's fields are not the instance's fields — and why `@ApplicationScoped` beans must not declare `final` methods. `@RequestScoped` binds an instance to the current request context (HTTP request in REST, message in messaging).

Pseudo-scopes skip the proxy: `@Singleton` injects the one instance directly (fast, but no contextual lifecycle and no per-request semantics), `@Dependent` creates a fresh instance per injection point and matches Spring's prototype most closely. Because `@Dependent` is the default, an unannotated bean discovered by ArC behaves like "new per injection" — the usual source of "my service was constructed twice" surprises.

```java
// Bean scopes observable in a running app (JDK 21, Quarkus 3.39.2, mvn test green).
package org.acme.check;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.context.Dependent;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;

@Singleton
class EagerSingleton {
    String id() { return "singleton@" + Integer.toHexString(hashCode()); }
}

@Dependent
class PerInjection {
    String id() { return "dependent@" + Integer.toHexString(hashCode()); }
}

@ApplicationScoped
class ScopeProbe {
    @Inject EagerSingleton single;      // real instance injected (pseudo-scope)
    @Inject PerInjection fresh;         // new instance for this injection point
    @Inject ScopeProbe self;            // client proxy (normal scope)
    String report() {
        return single.id() + " | " + fresh.id() + " | proxy=" + (self != this);
    }
}
// report() (verbatim, QuarkusTest run):
// singleton@6a5c2d2d | dependent@1dadd172 | proxy=true
// Called twice, the singleton id repeated (one shared instance), the dependent id also
// repeated - @Dependent is per INJECTION POINT, not per method call - and self != this
// stayed true: the proxy delegates method calls, it is not the instance.
```

**Listing 1.** Pseudo-scopes hand out real instances at injection time; a normal scope hands out a proxy whose identity differs from the target instance. Counters on injected beans must be read through methods, never fields — a proxy does not delegate field access.

```d2
direction: right
inject: "Injection point" {
  width: 160
  height: 50
}
normal: "Normal scope\n@ApplicationScoped, @RequestScoped" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "Client proxy\nlazy: instance on first call" {
  width: 250
  height: 70
  style.fill: "#fff3e0"
}
pseudo: "Pseudo scope\n@Dependent, @Singleton" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
inst1: "one contextual instance\nper application/request" {
  width: 280
  height: 60
}
inst2: "new instance per injection point\nor a single shared instance" {
  width: 290
  height: 60
}
inject -> normal -> proxy -> inst1
inject -> pseudo -> inst2
```

**Fig. 1.** The scope decides both the object you actually hold (proxy or instance) and the lifetime behind it — the two questions an interviewer follows up with.

## Scope boundaries and extras

ArC resolves the container at build time over one annotated-discovery bean archive; scopes themselves are standard CDI qualifiers, but a few container features differ from a full application server: there is no conversation context, `@SessionScoped` beans need the servlet extension, and unused beans are removed during build unless `quarkus.arc.remove-unused-beans` keeps them ([[What is Jandex in Quarkus]]). Quarkus-owned scopes appear where a context naturally exists — `jakarta.transaction.TransactionScoped` for the active transaction, `io.vertx.ext.web.@LocationScoped` for a routed Vert.x request — and `@Startup` forces early instantiation of an `@ApplicationScoped` bean ([[How do you run code at application startup in Quarkus]]).

> [!warning] "Singleton is the strictest scope" — backwards
> In CDI `@Singleton` is a *pseudo*-scope: one instance, but no proxy, no interception of contextual semantics, and it is instantiated eagerly at injection even if the bean is never used afterward. `@ApplicationScoped` is the stronger contextual guarantee with lazy proxy access. Mixing them up produces wrong claims about thread safety too — neither scope makes a bean thread-safe; concurrent methods still see shared mutable state.

> [!tip] Interview answer
> In Quarkus the CDI scope set applies: normal scopes — ApplicationScoped and RequestScoped — inject a client proxy and instantiate lazily on first method call; pseudo-scopes — Dependent and Singleton — inject real instances at injection time, Dependent being the per-injection default. Session scope only exists with a servlet stack, and Quarkus adds TransactionScoped and Vert.x location scopes. The proxy detail matters: fields on an injected ApplicationScoped bean are the proxy's fields, so state goes through methods.
