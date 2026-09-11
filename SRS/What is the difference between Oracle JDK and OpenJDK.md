<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What is the difference between Oracle JDK and OpenJDK

> [!abstract] Short answer
> **OpenJDK is the open-source reference implementation (GPL v2 + Classpath Exception) of the Java SE specification; Oracle JDK is Oracle's product build of those same sources.** Since JDK 11 the two are feature-identical per release — the real difference is **license and support**: Oracle JDK changed commercial terms in 2019 (8u211+/11), went free again under the NFTC license for 17+, and moved to a per-employee "Java SE Universal" subscription in 2023; meanwhile other vendors ship certified OpenJDK builds (Temurin, Corretto, Zulu, Liberica, GraalVM).

## Lineage and what actually differs

Sun open-sourced the platform as OpenJDK in 2006–2007; Oracle inherited it in 2010 and built Oracle JDK from it, adding commercial extras (Mission Control, installers, fonts, longer support contracts). Differences like Flight Recorder and Mission Control were open-sourced by 11, and since then the release notes describe the two as essentially the same code with different licensing and support. The runtime can only report its **build identity** — `java.vendor`, `java.vm.name` — which is exactly how you tell which build you are on ([[What is an LTS release of Java]], [[What is the Java release cadence since Java 9]]).

The licensing history is the interview-grade part: JDK 8 before 8u211 and JDK 11 pre-GA were usable commercially under the Oracle BCL/OTN mix; the 2019 OTN change made production use of Oracle JDK paid, which is what pushed the industry onto community builds (Temurin 8/11); NFTC made 17 (and later 21, 25) free again for a window; the 2023 per-employee subscription is why companies track Oracle vs non-Oracle builds. All builds pass the same TCK certification to call themselves "Java SE compatible."

```d2
direction: down
spec: "Java SE Specification (JCP)" {
  width: 300
  height: 50
}
oj: "OpenJDK source tree\nGPL v2 + CE" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
o: "Oracle JDK\nNFTC / OTN license, support contract" {
  width: 320
  height: 65
  style.fill: "#fff8e1"
}
v: "Vendor builds: Temurin, Corretto,\nZulu, Liberica, GraalVM" {
  width: 340
  height: 65
  style.fill: "#e8f5e9"
}
spec -> oj
oj -> o
oj -> v
```

**Fig. 1.** One source tree and one specification; Oracle JDK and the vendor builds are different distributions of the same code, distinguished by license and support.

```java
public class V07_OpenJdk {
    public static void main(String[] args) {
        System.out.println("java.vendor: " + System.getProperty("java.vendor"));
        System.out.println("java.vendor.url: " + System.getProperty("java.vendor.url"));
        System.out.println("java.vm.vendor: " + System.getProperty("java.vm.vendor"));
        System.out.println("java.vm.name: " + System.getProperty("java.vm.name"));
        System.out.println("java.specification.vendor: " + System.getProperty("java.specification.vendor"));
        System.out.println("java.version: " + System.getProperty("java.version"));
    }
}
```

**Listing 1.** Verified on JDK 21 (V07_OpenJdk in empirics): `java.vendor: Eclipse Adoptium`, `java.vm.name: OpenJDK 64-Bit Server VM`, `java.specification.vendor: Oracle Corporation` — this is a Temurin (community OpenJDK) build of the Oracle-led specification; one platform, many vendors (out/V07_OpenJdk.txt).

> [!warning] "OpenJDK is a different Java" is the popular lie
> OpenJDK is not a dialect or a lighter fork — it is the implementation the spec is developed against, and post-11 Oracle JDK contains no meaningful feature advantage. The genuine risks are elsewhere: (1) licensing — Oracle's free-use terms changed in 2019 and 2023, and "free for now" NFTC windows close when the next LTS ages out; (2) support duration — community builds have no contractual SLA; (3) branding — `java.vendor` identifies the build, not a feature level, so do not infer capability from vendor name.

> [!tip] Interview answer
> **OpenJDK is the GPL+CE reference implementation; Oracle JDK is Oracle's product build of the same code — feature-equal since 11.** The difference is license and support: Oracle went commercial in 2019, free again for 17+ under NFTC, then per-employee pricing in 2023, while Temurin/Corretto/Zulu ship certified builds. I pick by support needs and license exposure, not by technical myth.
