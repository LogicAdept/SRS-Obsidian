<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What is an LTS release of Java

> [!abstract] Short answer
> **LTS (Long-Term Support) is a vendor support designation, not a technical property of the JDK.** Since the six-month cadence began, Oracle and the wider ecosystem designate every second September release as LTS: **8, 11, 17, 21, 25** — the next planned LTS is **29** (September 2027). Feature releases between them get fixes for roughly one cycle; LTS builds get security and stability updates for years, which is why production deploys them.

## What the label actually buys

An LTS release carries no extra features — it is the same platform as the surrounding trains. What it buys is **time**: vendors (Oracle Premier/Extended Support, Eclipse Temurin, Amazon Corretto, Azul, BellSoft, Red Hat) publish support windows measured in years and backport security fixes. Oracle's roadmap, for example, keeps Premier Support for 8, 11, 17, 21, and 25 with Extended Support for 8 running past 2030. The version you pull is a **build identity** — vendor plus version — and identity is all the runtime itself can tell you ([[What is the difference between Oracle JDK and OpenJDK]], [[How does Java version numbering work]]).

Interview framing: LTS is where risk-averse deployments live; the feature trains in between are where new APIs and previews are evaluated ([[What is the Java release cadence since Java 9]], [[What is a preview feature in Java]]). Naming the LTS spine plus one real production fact per line is the credible answer to "which versions have you used."

```d2
direction: down
lts: "LTS spine — vendor-patched for years" {
  shape: rectangle
  v8: "8   GA Mar 2014"
  v11: "11  GA Sep 2018"
  v17: "17  GA Sep 2021"
  v21: "21  GA Sep 2023"
  v25: "25  GA Sep 2025"
  v8 -> v11 -> v17 -> v21 -> v25
}
feat: "between: 9–10, 12–16, 18–20, 22–24, 26…\none fix cycle each" {
  shape: rectangle
}
```

**Fig. 1.** Five LTS boxes so far, roughly two years apart; the non-LTS trains fill the gaps and are superseded, not serviced.

```java
public class V02_Lts {
    public static void main(String[] args) {
        System.out.println("java.version: " + System.getProperty("java.version"));
        System.out.println("java.vendor: " + System.getProperty("java.vendor"));
        System.out.println("java.vm.name: " + System.getProperty("java.vm.name"));
        System.out.println("java.specification.version: " + System.getProperty("java.specification.version"));
    }
}
```

**Listing 1.** Verified on JDK 21 (V02_Lts in empirics): `java.version: 21.0.12.1`, `java.vendor: Eclipse Adoptium`, `java.vm.name: OpenJDK 64-Bit Server VM`, `java.specification.version: 21`. The runtime knows its build identity — the LTS label and support dates live in the vendor's policy, not in the JVM (out/V02_Lts.txt).

> [!warning] LTS is a contract, not a feature list
> Two traps: first, "LTS" dates differ per vendor — Oracle Premier, Temurin community support, and Corretto commitments are different policies over different years; quoting Oracle's dates as universal facts is wrong. Second, vendors may name non-LTS builds anything they like and still patch forks privately — but the standard train stops. And `21.0.12.1+1-LTS` in a version string is vendor naming decoration; nothing in the JVM specification defines "LTS" ([[What is the Java release cadence since Java 9]]).

> [!tip] Interview answer
> **LTS is the vendor support designation for 8, 11, 17, 21 and 25 — same platform, but years of security backports, which is what production runs.** Non-LTS trains live for one cycle. I deploy on LTS lines and evaluate trains in between; the label comes from the vendor roadmap, not the JVM.
