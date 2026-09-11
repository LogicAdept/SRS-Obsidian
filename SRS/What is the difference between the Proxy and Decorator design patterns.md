<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What is the difference between the Proxy and Decorator design patterns

> [!abstract] Short answer
> Same wrapper structure, **different intent and lifecycle control**. A Proxy implements the same interface as its service and **controls access** to it — lazy initialization, caching, protection, remote calls — usually creating and managing the service itself. A Decorator **adds behavior** in layers, and the client assembles and owns the composition.

## Intent first, mechanics second

Both patterns are built on composition: one object holds a reference to another behind a shared interface and delegates. The catalog's one-line contrast is about interfaces across the whole wrapper family: with Adapter you access an object via a different interface, with Proxy the interface stays the same, with Decorator you access it via an enhanced interface. The sharper difference for Proxy versus Decorator is who manages the target. A virtual proxy creates the heavyweight service on first use and may dismiss it later; a caching proxy owns the cache and its invalidation; a protection proxy checks credentials before letting any call through. Decorator layers, by contrast, are composed by the client, which decides how many wrappers to apply and in what order — the wrapper stack has no lifecycle responsibility for the object inside.

```d2
direction: right
proxy: "Proxy\nsame interface\nowns the service lifecycle" { width: 240; height: 100; style.fill: "#e3f2fd" }
decorator: "Decorator\nsame interface\nclient assembles layers" { width: 240; height: 100; style.fill: "#fff3e0" }
adapter: "Adapter\ndifferent interface\ntranslates calls" { width: 220; height: 100; style.fill: "#e8f5e9" }
proxy -> decorator -> adapter: intent spectrum
```

**Fig. 1.** The three same-shape wrappers read as an intent spectrum: control access, extend behavior, or change the interface.

## Recognizing them in real code

In Java the distinction shows up in the ecosystem. `java.lang.reflect.Proxy` and Spring AOP proxies implement the target interface to intercept calls for transactions, security, or remoting — access control in the Proxy sense. The `InputStream` wrapper family — `BufferedInputStream`, `CipherInputStream` — is Decorator: each adds behavior and the application code stacks them. Both wrap, both delegate, and both keep the interface, so the deciding question in an interview is who creates the wrapped object and why the wrapper exists. Each side has its own card — [[How would you explain the Decorator design pattern]] — while [[How would you explain the Adapter design pattern]] completes the trio and [[What are examples of structural design patterns]] surveys the family.

> [!warning] "Proxy is just a Decorator with the same interface" loses the point
> The catalog explicitly notes the structures are similar while the intents are very different, and the lifecycle ownership is the observable proof: a proxy typically constructs, substitutes, and releases its service on its own, while a decorator never decides when its wrappee exists — the client already built that stack.

> [!tip] Interview answer
> Proxy and Decorator share the wrapper structure and keep the target interface. Proxy exists to control access — virtual, caching, protection, remote — and usually manages the service's full lifecycle itself. Decorator exists to add behavior in composable layers that the client assembles. So: same mechanics, different intent, and the practical tell is who creates and controls the wrapped object.
