<!--
reps: 0
priority: 0
-->
#Java/Versions/15 #SRS

# What was new in Java 15

> [!abstract] Short answer
> **Java 15 (September 2020) finalized text blocks (JEP 378), previewed sealed classes (360), moved ZGC (377) and Shenandoah (379) to production, removed Nashorn (372), added hidden classes (371) and EdDSA signatures (339), disabled biased locking (374), reimplemented DatagramSocket on NIO (373), and deprecated RMI Activation (385) plus the Solaris/SPARC ports (381). Records and instanceof patterns were still previews here.**

## Text blocks final, collectors production, Nashorn gone

Text blocks graduated to standard — the syntax stopped moving ([[What are text blocks]]). The two low-latency collectors left "experimental" behind: production-ready ZGC and Shenandoah mean support contracts and fewer flags, not defaults — G1 stayed the default collector ([[What is the default garbage collector by Java version]]). Hidden classes (371) gave frameworks a supported way to define classes that are not discoverable by name — the supported basis for dynamic proxies and language runtimes, replacing `sun.misc.Unsafe::defineAnonymousClass`. EdDSA (339) brought a modern signature scheme into the standard crypto provider. Nashorn removal (372, deprecated in 11 by JEP 335) ended the built-in JavaScript engine — `javax.script` users had to add GraalJS or similar ([[What is Nashorn]]).

```java
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

public class V31_EdDsa15 {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator g = KeyPairGenerator.getInstance("Ed25519");  // JEP 339, JDK 15
        KeyPair kp = g.generateKeyPair();
        Signature sig = Signature.getInstance("Ed25519");
        sig.initSign(kp.getPrivate());
        sig.update("jdk15".getBytes());
        byte[] s = sig.sign();
        sig.initVerify(kp.getPublic());
        sig.update("jdk15".getBytes());
        System.out.println("Ed25519 verify=" + sig.verify(s) + " sigBytes=" + s.length);
        System.out.println("alg=" + kp.getPublic().getAlgorithm());
    }
}
```

**Listing 1.** Verified on JDK 21 (V31_EdDsa15 in empirics): `Ed25519 verify=true sigBytes=64`, `alg=EdDSA` (out/V31_EdDsa15.txt).

```d2
direction: right
lang: "text blocks FINAL (378)\nsealed PREVIEW (360)" { style.fill: "#e8f5e9"; width: 220; height: 80 }
coll: "ZGC production (377)\nShenandoah production (379)" { style.fill: "#e3f2fd"; width: 240; height: 80 }
gone: "Nashorn REMOVED (372)\nRMI Activation deprecated (385)" { style.fill: "#ffebee"; width: 260; height: 80 }
lang -> coll -> gone: ""
```

**Fig. 1.** Java 15: the language line stabilizes, both low-latency collectors go production, and legacy JavaScript/RMI-activation surface starts leaving.

> [!warning] "Production" for a collector is not "default"
> After 15, ZGC and Shenandoah were supported but you still had to opt in with `-XX:+UseZGC` / `-XX:+UseShenandoahGC`; G1 remained the default until today. Also, 15 is where Nashorn disappeared: code calling `new NashornScriptEngineFactory()` broke, and the `jjs` tool was gone ([[What is jjs]]).

> [!tip] Interview answer
> **Java 15 finalized text blocks, previewed sealed classes, and made ZGC and Shenandoah production-ready while removing Nashorn. It added hidden classes for framework use, EdDSA signatures, and disabled biased locking as no longer worth the maintenance. Sealed classes finalized two trains later in 17.**
