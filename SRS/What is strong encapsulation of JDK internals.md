<!--
reps: 0
priority: 0
-->
#Java/Versions/16 #SRS

# What is strong encapsulation of JDK internals

> [!abstract] Short answer
> **Strong encapsulation is the JPMS endgame for JDK internals: non-exported platform packages (the `sun.*`/`com.sun.*` internals, `java.lang`'s private fields) are inaccessible to reflection unless the owning module `opens` them or you pass `--add-opens`.** The rollout: JDK 9 warned (`--illegal-access=permit` default), JDK 16 made denial the default (JEP 396), JDK 17 removed the `--illegal-access` switch entirely (JEP 403) — `setAccessible(true)` on an unopened internal throws `InaccessibleObjectException` ([[What is the Java Platform Module System]]).

## The timeline and the flag that works

Java 9 (JEP 260) encapsulated most internals but permitted deep reflection with a warning. Java 15 flipped the default per JEP 396's draft debates, and **16** (JEP 396) made `--illegal-access=deny` the default; **17** (JEP 403) deleted the flag altogether — the only escape hatch left is `--add-opens java.base/java.lang=ALL-UNNAMED` (or `--add-exports` for compile-time/accessible-member access without deep reflection). The `java.base` module does **not** open `java.lang`, so `String.class.getDeclaredField("value").setAccessible(true)` fails — this is the canonical demo and the canonical production crash for old Hibernate, Jackson, and mockito versions ([[What does setAccessible do in the Reflection API]]).

Not everything moved: `sun.misc.Unsafe` still exists (deprecated for removal via JEP 471's deprecation path and replaced by the Foreign Function & Memory API), and `jdk.unsupported` keeps legacy bridges alive. The upgrade playbook is: upgrade the offending library; if impossible, add a targeted `--add-opens` per package — blanket opens on production JVMs are config debt ([[What was removed or deprecated in Java 17]]).

```d2
direction: down
j9: "JDK 9 (JEP 260)\ndeep reflection works, warns" {
  width: 300
  height: 65
  style.fill: "#fff8e1"
}
j16: "JDK 16 (JEP 396)\n--illegal-access=deny default" {
  width: 320
  height: 65
  style.fill: "#fff3e0"
}
j17: "JDK 17 (JEP 403)\n--illegal-access removed;\nonly --add-opens / --add-exports" {
  width: 360
  height: 85
  style.fill: "#ffcdd2"
}
ok: "--add-opens java.base/java.lang=ALL-UNNAMED\n-> setAccessible works" {
  width: 400
  height: 65
  style.fill: "#e8f5e9"
}
j9 -> j16 -> j17 -> ok: "fix"
```

**Fig. 1.** Three steps to sealed internals: warn, deny by default, remove the switch. The surviving escape hatch is a targeted `--add-opens`.

```java
import java.lang.reflect.Field;

public class V20_Encapsulation {
    public static void main(String[] args) throws Exception {
        Field value = String.class.getDeclaredField("value");
        try {
            value.setAccessible(true);
            System.out.println("setAccessible(true) succeeded: canAccess=" + value.canAccess("x"));
        } catch (java.lang.reflect.InaccessibleObjectException e) {
            System.out.println("InaccessibleObjectException: " + e.getMessage());
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V20_Encapsulation in empirics), default flags: `InaccessibleObjectException: Unable to make field private final byte[] java.lang.String.value accessible: module java.base does not "opens java.lang" to unnamed module @15db9742`. The same class run with `--add-opens java.base/java.lang=ALL-UNNAMED` prints `setAccessible(true) succeeded: canAccess=true` (out/V20_Encapsulation.txt, out/V20_Encapsulation_addopens.txt).

> [!warning] --illegal-access is gone; blanket --add-opens is not a strategy
> The interview traps: recommending `--illegal-access=permit` on 17+ fails — the JVM rejects the removed switch (JEP 403). Saying "reflection is broken in Java 17" overreaches — reflection on your own classes and on *opened* packages is untouched; only unopened internals are sealed. And adding `--add-opens java.base/**=ALL-UNNAMED` for everything silences today's error while recreating exactly the coupling strong encapsulation exists to remove — upgrade the library first ([[What are the typical problems when upgrading from Java 8 to 17]]).

> [!tip] Interview answer
> **Strong encapsulation sealed JDK internals: 9 warned, 16 denied by default (JEP 396), 17 removed the --illegal-access escape (JEP 403) — setAccessible on unopened internals now throws InaccessibleObjectException.** The fix is upgrading libraries, or targeted `--add-opens` per package. I demo it with String's `value` field: fails on 21, passes with the open.
