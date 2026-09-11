<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What is the Java release cadence since Java 9

> [!abstract] Short answer
> **One feature JDK every six months, always March and September; long-term-support (LTS) releases land every two years on the September train.** A feature release (9, 10, 12–16, 18–20, 22–24, 26) is superseded as soon as the next JDK ships — it gets fixes only in that one cycle. LTS releases (8, 11, 17, 21, 25, next 29) are the ones vendors patch and shops deploy for years.

## How the train works

Since JDK 9 the JDK follows a strict time-based model (JEP 322): the feature release date is fixed and features ride or wait — a half-finished feature slips to the next train instead of delaying the release. Each release goes through milestones: Rampdown Phase One, Rampdown Phase Two, Release Candidates, then General Availability in the third week of the release month. Every six months a JDK ships; every fourth one (since 8) is designated LTS and gets multi-year security and bug-fix updates from vendors ([[What is an LTS release of Java]], [[Which Java versions have you used professionally]]).

The consequence interviewers probe: a non-LTS version is not "dead on arrival," but after 12 months no more patches ship for it — production sticks to LTS builds, while feature releases are where previews and new APIs are tried ([[What is a preview feature in Java]], [[What is an incubator module]]). As of September 2026 the current feature release is 26 (GA 17 March 2026) and 27 is the September 2026 train; the latest LTS is 25.

```d2
direction: right
sep21: "Sep 2023\n21 (LTS)" {
  width: 190
  height: 60
  style.fill: "#e8f5e9"
}
sep24: "Sep 2024\n22, 23, 24\nnon-LTS" {
  width: 200
  height: 70
  style.fill: "#fff8e1"
}
sep25: "Sep 2025\n25 (LTS)" {
  width: 190
  height: 60
  style.fill: "#e8f5e9"
}
sep26: "Mar 2026\n26 / Sep 2026: 27\nnon-LTS" {
  width: 210
  height: 70
  style.fill: "#fff8e1"
}
sep27: "Sep 2027\n29 (LTS, planned)" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
sep21 -> sep24 -> sep25 -> sep26 -> sep27
```

**Fig. 1.** The two-year LTS spine (green) with six-month feature trains between. A non-LTS JDK is replaced, not maintained, once the next one ships.

```java
public class V01_Cadence {
    public static void main(String[] args) {
        Runtime.Version v = Runtime.version();
        System.out.println("Runtime.version(): " + v);
        System.out.println("feature(): " + v.feature());
        System.out.println("interim(): " + v.interim());
        System.out.println("update(): " + v.update());
        System.out.println("specification: " + System.getProperty("java.specification.version"));
        List.of("Mar 2026 -> 26", "Sep 2026 -> 27").forEach(s -> System.out.println("train: " + s));
    }
}
```

**Listing 1.** Verified on JDK 21 (V01_Cadence in empirics): `Runtime.version(): 21.0.12.1+1-LTS`, `feature(): 21`, `interim(): 0`, `update(): 12`, `specification: 21` — the `-LTS` marker is the vendor build's naming, the numbers come from JEP 322 versioning (out/V01_Cadence.txt).

> [!warning] "Nobody runs Java 10" is by design, not scandal
> A feature release stops receiving updates when the next one lands, so saying "10 was abandoned" misunderstands the model — it was never meant to be a long stop. The reverse lie is also common: claiming you "run Java 19 in production" on a vendor with no 19 support line. Production answers name LTS builds; previews and feature releases are evaluation territory. Also do not say "Java 9 had two years of support" — support length is a vendor contract, not a JDK property ([[What is an LTS release of Java]]).

> [!tip] Interview answer
> **Since Java 9 a JDK ships every six months (March and September), features land when ready and slip otherwise; every second September release is LTS — 8, 11, 17, 21, 25, next 29.** Non-LTS releases are superseded after one cycle; production runs LTS builds. I upgrade via LTS lines and evaluate new features on the trains.
