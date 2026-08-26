<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is an AOP proxy in Spring?

> [!abstract] Short answer
> An **AOP proxy** is the object Spring creates at **runtime** to implement aspect contracts: clients call the **proxy**, interceptors (advice) run, then the call reaches the **target**. It is a **JDK dynamic proxy** (interfaces) or a **CGLIB subclass**. The container injects the **proxy**, not the raw instance. Self-calls on `this` never hit it.

## Runtime stand-in for the target

Spring *AOP Concepts*: an AOP proxy implements aspect contracts (advice method executions). Spring uses **JDK dynamic proxies** or **CGLIB**. *Proxying Mechanisms*: if the target implements **at least one interface**, a **JDK** proxy covers those interfaces; if **no** interfaces, a **CGLIB** subclass is generated.

That is the **core Framework** default. **Spring Boot** may enable **class-based (CGLIB) proxies by default** (`spring.aop.proxy-target-class`). Force CGLIB with `proxyTargetClass=true` / `<aop:aspectj-autoproxy proxy-target-class="true"/>`.

```d2
direction: right
client: "Caller" {
  width: 120
  height: 50
  style.fill: "#e3f2fd"
}
proxy: "AOP proxy\n(JDK or CGLIB)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
adv: "Advice chain" {
  width: 140
  height: 50
  style.fill: "#fce4ec"
}
target: "Target bean" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}

client -> proxy -> adv -> target
```

**Fig. 1.** Only calls that enter the proxy are advised — [[Why does a self-invocation skip Spring AOP advice]]. Kinds and tradeoffs: [[What kinds of proxies exist in Java or Spring]], [[What are Spring AOP proxy limitations]].

> [!warning] `this.foo()` is not a proxy call
> After the target is entered, `this` is the real object. Inner method advice does not run.

> [!warning] Do not assume CGLIB everywhere
> Framework docs: **interface → JDK proxy**. Boot often flips the global default to CGLIB. Final classes/methods and private methods still cannot be advised via subclassing.

> [!tip] Interview answer
> **The AOP proxy is the runtime object that wraps a Spring bean so advice can run.** JDK proxy if there is an interface (Framework default); CGLIB subclass otherwise — Boot often uses CGLIB by default. Callers get the proxy from the container; `this` inside the target bypasses it.
