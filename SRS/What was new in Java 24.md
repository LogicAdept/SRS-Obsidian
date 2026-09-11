<!--
reps: 0
priority: 0
-->
#Java/Versions/24 #SRS

# What was new in Java 24

> [!abstract] Short answer
> **Java 24 (March 2025) finalized stream gatherers (JEP 485) and the Class-File API (484), permanently disabled the Security Manager (486), made `synchronized` on virtual threads pin-free (491), experimented with compact object headers (450) and AOT class loading & linking (483), removed ZGC non-generational mode (490), and added post-quantum crypto ML-KEM (496) / ML-DSA (497). Generational Shenandoah appeared experimentally (404).**

## The pinning fix and the security cleanup

JEP 491 is the one virtual-thread users felt immediately: blocking inside `synchronized` blocks no longer pins the carrier thread — the monitor is armed differently so the virtual thread can unmount, which un-blocked the classic "synchronized around a JDBC call starves my carrier pool" failure mode ([[How would you explain Virtual Threads]]). JEP 486 finished Security Manager: deprecated for removal in 17 (411), it now cannot be enabled at all — `-Djava.security.manager=allow` is ignored, `System.setSecurityManager` always throws ([[What happened to the Security Manager across Java versions]]). Gatherers (485) gave `Stream.gather` as the general custom-intermediate-operation API ([[What are stream gatherers]]); the Class-File API (484) replaced ASM-era bytecode parsing with an official, version-proof library. Compact object headers (450) previewed the Lilliput memory cut, product-ready in 25 ([[What are compact object headers]]).

```java
import java.security.KeyPairGenerator;

public class V37_MlKem24 {
    public static void main(String[] args) throws Exception {
        try {
            KeyPairGenerator.getInstance("ML-KEM-512");   // JEP 496, JDK 24
            System.out.println("ML-KEM-512 available");
        } catch (java.security.NoSuchAlgorithmException e) {
            System.out.println("ML-KEM-512 -> NoSuchAlgorithmException on this JDK");
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V37_MlKem24 in empirics): `ML-KEM-512 -> NoSuchAlgorithmException on this JDK` (out/V37_MlKem24.txt) — the post-quantum KEM family is a Java 24 fact, absent in 21.

```d2
direction: right
fin: "gatherers FINAL (485)\nClass-File API FINAL (484)" { style.fill: "#e8f5e9"; width: 260; height: 80 }
vt: "sync VT without pinning (491)\nAOT class loading (483)" { style.fill: "#e3f2fd"; width: 260; height: 80 }
gone: "Security Manager DISABLED (486)\nZGC non-gen mode REMOVED (490)" { style.fill: "#ffebee"; width: 300; height: 80 }
exp: "compact headers EXP (450)\nShenandoah generational EXP (404)\nML-KEM / ML-DSA (496/497)" { style.fill: "#fff3e0"; width: 320; height: 100 }
fin -> vt -> gone -> exp: ""
```

**Fig. 1.** Java 24: two finals, the pinning fix, security cleanup, and a bench of experiments that 25 industrializes.

> [!warning] Vendor builds differ on the experimental bench
> Compact object headers and generational Shenandoah shipped in 24 as experimental flags — presence and defaults vary by vendor and build. The security story, though, is uniform: after 486 there is no flag, no compatibility mode, no vendor knob — Security Manager is simply gone ([[What happened to the Security Manager across Java versions]]).

> [!tip] Interview answer
> **Java 24 finalized stream gatherers and the Class-File API, fixed virtual-thread pinning inside synchronized, and permanently disabled the Security Manager. It experimented with compact object headers and AOT class loading, removed ZGC non-generational mode, and added post-quantum ML-KEM/ML-DSA. For Loom users, 491 is the release that made synchronized safe to keep.**
