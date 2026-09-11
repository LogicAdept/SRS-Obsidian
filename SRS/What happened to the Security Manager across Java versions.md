<!--
reps: 0
priority: 0
-->
#Java/Versions/24 #SRS

# What happened to the Security Manager across Java versions

> [!abstract] Short answer
> **Deprecated for removal in Java 17 (JEP 411), the Security Manager was permanently disabled in Java 24 (JEP 486): it can no longer be installed — `-Djava.security.manager=allow` is ignored, `System.setSecurityManager` always throws `UnsupportedOperationException` — and the API stays as an inert shell. The sandbox use case moved to OS and container isolation.**

## The timeline and the reasoning

17 (411) flipped the switch to terminal deprecation: installing required the `allow` property and printed warnings, signaling "migrate now". 24 (486) completed it: no installation path exists, `AccessController` checks became no-ops, while the classes remain so old code still loads. The rationale, argued across JEP 411: the Security Manager never delivered real containment — malicious code found escape hatches (reflection timing, finalizer attacks, native calls), and modern isolation happens outside the JVM process: containers, VMs, OS users. Library cleanup followed: permission checks and `doPrivileged` blocks were stripped from the JDK over subsequent releases ([[What was removed or deprecated in Java 17]] has the 17-side inventory).

```java
public class V54_SecurityManager {
    public static void main(String[] args) {
        System.out.println("java.security.manager=" + System.getProperty("java.security.manager", "<unset>"));
        try {
            System.setSecurityManager(new SecurityManager());
            System.out.println("installed=" + (System.getSecurityManager() != null));
        } catch (UnsupportedOperationException e) {
            System.out.println("setSecurityManager -> UnsupportedOperationException");
        }
    }
}
```

**Listing 1.** Verified on JDK 21, two runs (V54_SecurityManager in empirics): default — `java.security.manager=<unset>`, `setSecurityManager -> UnsupportedOperationException`; with `-Djava.security.manager=allow` — `java.security.manager=allow`, `WARNING: A terminally deprecated method in java.lang.System has been called`, `installed=true` (out/V54_SecurityManager.txt). On 24 the `allow` path is gone entirely.

```d2
direction: right
j17: "Java 17 (411)\ndeprecated for removal;\ninstall needs allow flag" { style.fill: "#fff3e0"; width: 260; height: 90 }
j24: "Java 24 (486)\nPERMANENTLY DISABLED;\nno install path, inert API" { style.fill: "#ffebee"; width: 290; height: 90 }
iso: "sandboxing moved to\ncontainers / OS / VMs" { style.fill: "#e8f5e9"; width: 280; height: 80 }
j17 -> j24 -> iso: ""
```

**Fig. 1.** Two-step exit: a deprecation grace period from 17, hard disablement in 24, with the use case replaced outside the JVM.

> [!warning] The 21 behavior is already "broken by default"
> On 21 without flags, `setSecurityManager` throws — code that still installs one works only where operators opted in with `allow`. After 24 there is no opt-in, and `AccessController.doPrivileged` is a wrapper with no effect, so libraries sprinkling it "just in case" are cargo-culting ([[What is a helpful NullPointerException]] is the other runtime-message modernization of this era).

> [!tip] Interview answer
> **Security Manager was deprecated for removal in 17 and permanently disabled in 24: it cannot be installed anymore, doPrivileged is a no-op, the classes linger for compatibility. The reasoning: it never gave real containment, and isolation moved to containers and OS primitives. On 21 it already fails without the allow flag — the hard cutoff is 24.**
