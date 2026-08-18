<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`java.lang.reflect.Proxy` creates a class at runtime that implements one or more **interfaces** and forwards calls to an `InvocationHandler`.

```java
InvocationHandler handler = new MyInvocationHandler();
MyInterface proxyInstance = (MyInterface) Proxy.newProxyInstance(
    MyInterface.class.getClassLoader(),
    new Class<?>[] { MyInterface.class },
    handler);
```

Spring dumps elsewhere: JDK dynamic proxy if the bean has an interface; CGLIB if it does not. This card is the Reflection API `Proxy` type.

> [!warning] Unverified traps from the dump
> - JDK `Proxy` is interface-only in this dump — not a subclass of a concrete class.
> - There is no `#Java` child leaf yet for dynamic proxies.
