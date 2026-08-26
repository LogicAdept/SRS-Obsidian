<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is a Target object in Spring AOP?

> [!abstract] Short answer
> The **target** (also **advised object**) is the **original bean** that aspects apply to — the instance **behind** the AOP proxy. Callers normally hold the **proxy**. `JoinPoint.getTarget()` is that object; **`getThis()` is the proxy**. Calls on `this` inside the target skip advice.

## Advised object vs proxy

Spring *AOP Concepts*: **Target object** — an object being advised by one or more aspects; also called the advised object. Because Spring AOP uses **runtime proxies**, this object is **always a proxied object** (there is a proxy in front of it).

*Proxying Mechanisms*: the client’s reference is the **proxy**. After interceptors run, the call reaches the target (`SimplePojo`). Further `this.bar()` invokes the **target**, not the proxy.

Spring AOP `this` vs `target` PCDs: **`this`** matches the **proxy**; **`target`** matches the **application object being proxied**. Same split on `JoinPoint.getThis()` / `getTarget()` — [[What is the purpose of the JoinPoint interface in Spring AOP]].

```d2
direction: right
caller: "Injected reference" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
proxy: "AOP proxy\n(this)" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
target: "Target / advised object" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}

caller -> proxy -> target
```

**Fig. 1.** Container injects the proxy; the target is the real instance. See [[What is an AOP proxy in Spring]], [[Why does a self-invocation skip Spring AOP advice]].

> [!warning] Logging `getThis().getClass()` is often the proxy type
> CGLIB names look like `OrderService$$SpringCGLIB$$0`. Use `getTarget()` (or `AopUtils.getTargetClass`) for the domain class.

> [!warning] `target` is null for some join points
> AspectJ: `getTarget()` returns null when there is no target (for example static methods). Do not NPE on it.

> [!tip] Interview answer
> **The target is the real bean being advised; the proxy is what clients call.** Spring AOP always sits a proxy in front of that target. `getTarget()` / the `target` PCD refer to the bean; `getThis()` / `this` refer to the proxy. Self-invocation talks to the target and skips advice.
