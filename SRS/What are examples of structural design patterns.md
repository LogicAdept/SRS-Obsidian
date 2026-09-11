<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What are examples of structural design patterns

> [!abstract] Short answer
> The GoF structural set is seven patterns: **Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy**. Their common thread is assembling objects into larger structures while keeping the parts flexible — most of them are wrappers of one kind or another.

## The catalog set

Adapter lets objects with incompatible interfaces collaborate by translating calls. Bridge splits one class into two independent hierarchies — abstraction and implementation. Composite composes objects into tree structures that clients treat like single objects. Decorator attaches new behavior by wrapping an object in another object with the same interface. Facade exposes a simple entry point to a complex subsystem. Flyweight shares common state between many small objects to fit them into memory. Proxy provides a stand-in for a target and controls access to it — lazy initialization, caching, protection, remote calls.

## The wrapper family

Adapter, Decorator, and Proxy share the same mechanical shape: a class holding a reference to a wrapped object and delegating to it. What distinguishes them is intent. Adapter presents a different interface, Decorator keeps or extends the interface while layering behavior, and Proxy keeps the interface while controlling access — which is why [[What is the difference between the Proxy and Decorator design patterns]] is a standard interview follow-up after you name the wrapper family. The wrappers themselves are detailed in [[How would you explain the Adapter design pattern]] and [[How would you explain the Decorator design pattern]].

```d2
direction: right
a: "Adapter\nnew interface" { width: 180; height: 80; style.fill: "#e3f2fd" }
d: "Decorator\nsame interface,\nadded behavior" { width: 210; height: 80; style.fill: "#fff3e0" }
p: "Proxy\nsame interface,\ncontrolled access" { width: 210; height: 80; style.fill: "#e8f5e9" }
f: "Facade\none object for\na subsystem" { width: 200; height: 80; style.fill: "#e8f5e9" }
a -> d -> p: wrappers by intent
a -> f: vs simplification
```

**Fig. 1.** The wrapper family by intent: change the interface, extend the behavior, or control the access — Facade is the subsystem-wide cousin.

> [!warning] Same structure does not mean same pattern
> Saying "Decorator and Proxy are identical because both wrap" loses the interview point: intent and lifecycle control differ, and the catalog names exist to carry exactly that difference.

> [!tip] Interview answer
> Structural patterns: Adapter for incompatible interfaces, Bridge for independent abstraction and implementation hierarchies, Composite for uniform trees, Decorator for layered behavior, Facade for a simple entry to a subsystem, Flyweight for shared state at scale, Proxy for controlled access. Most are wrappers — the differences are intent, not structure.
