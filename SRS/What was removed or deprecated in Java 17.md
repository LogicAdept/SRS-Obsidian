<!--
reps: 0
priority: 0
-->
#Java/Versions/17 #SRS

# What was removed or deprecated in Java 17

> [!abstract] Short answer
> **Java 17 (September 2021, LTS) removed or terminally deprecated the legacy security and applet surface: SecurityManager and the access-controller API deprecated for removal (JEP 411), the Applet API deprecated for removal (JEP 398), experimental AOT/JIT compilers removed (JEP 410), RMI Activation already removed in 15 (JEP 385), Nashorn in 15 (JEP 372) — and it finished strong encapsulation of JDK internals (JEP 403) while finalizing sealed classes (JEP 409).** It is the "cleanup LTS": fewer footguns, harder edges.

## The inventory

**SecurityManager** (JEP 411) is deprecated for removal: installing one now requires `-Djava.security.manager=allow`, and `System::setSecurityManager` throws `UnsupportedOperationException` without it, plus a terminal-deprecation warning with it. The related `java.security.AccessController`/`doPrivileged` surface moved toward inertness. **Applet API** (JEP 398) — `java.applet` — is deprecated for removal and was deleted outright in 26 (JEP 504). **Experimental AOT/JIT** (JEP 410, Graal-based) left; the production path became GraalVM or later JDK AOT caches. **Strong encapsulation** (JEP 403) removed `--illegal-access`, sealing internals ([[What is strong encapsulation of JDK internals]]). **Sealed classes** finalized (JEP 409) — the one headline addition ([[How would you explain Sealed classes]]).

Neighbors worth one sentence each: RMI Activation (15, JEP 385), Nashorn and `jjs` (15, JEP 372), CMS collector (removed **14**, JEP 363) — interview answers often misplace these into 17 ([[What is Nashorn]], [[What is the default garbage collector by Java version]]).

```d2
direction: down
j17: "JDK 17" {
  shape: rectangle
  sec: "SecurityManager deprecated (411)\nsetSecurityManager needs allow-flag"
  app: "Applet API deprecated (398)"
  aot: "experimental AOT/JIT removed (410)"
  enc: "strong encapsulation done (403)"
  sea: "sealed classes final (409)"
}
before: "earlier removals often misattributed to 17" {
  shape: rectangle
  nash: "Nashorn + jjs -> 15"
  rmi: "RMI Activation -> 15"
  cms: "CMS GC -> 14"
}
```

**Fig. 1.** What 17 actually did to the platform, plus the earlier removals that get blamed on it — keep Nashorn (15), RMI Activation (15), CMS (14) in the right column.

```java
public class V21_Removed17 {
    public static void main(String[] args) {
        System.out.println("getSecurityManager(): " + System.getSecurityManager());
        try {
            System.setSecurityManager(new SecurityManager());
            System.out.println("setSecurityManager succeeded");
        } catch (UnsupportedOperationException e) {
            System.out.println("UnsupportedOperationException: " + e.getMessage());
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V21_Removed17 in empirics), default flags: `getSecurityManager(): null`, `UnsupportedOperationException: The Security Manager is deprecated and will be removed in a future release`. The same run with `-Djava.security.manager=allow` prints `setSecurityManager succeeded` — after terminal-deprecation warnings (out/V21_Removed17.txt, out/V21_Removed17_allow.txt).

> [!warning] Deprecation semantics are not removal semantics
> Three precision traps: deprecated-for-removal means **still present but gated** — SecurityManager code runs under `allow`, Applets still existed in 17 (removed in 26), and citing either as "removed in 17" is wrong. Second, JEP 411's deprecation does **not** make `setSecurityManager` fail on all setups — only without the allow flag; blanket claims fail the follow-up. Third, `javax`→`jakarta` migration is an ecosystem change with no JEP in 17 — pairing "Java 17 requires jakarta" in an answer is a correctness red flag ([[What Java EE modules were removed in Java 11]]).

> [!tip] Interview answer
> **Java 17 is the cleanup LTS: SecurityManager terminally deprecated (needs -Djava.security.manager=allow, else setSecurityManager throws), Applet API deprecated, experimental AOT removed, internals sealed by JEP 403 — plus sealed classes finalized.** Nashorn, RMI Activation, and CMS went earlier (15/15/14), not in 17.
