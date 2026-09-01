<!--
reps: 0
priority: 0
-->
#Java/Versions #Career/Java #Career/Experience #Career/Interview #SRS

# Which Java versions have you used professionally

> [!abstract] Short answer
> **Name the LTS lines you actually shipped on — usually a subset of 8, 11, 17, 21, 25 — and one production fact per line.** This is a résumé question, not a feature recitation. Oracle’s Java SE support roadmap (updated 4 Aug 2026) treats **8, 11, 17, 21, and 25 as LTS**; the next planned LTS is **29** (September 2027). Non-LTS feature releases (9–10, 12–16, 18–20, 22–24, 26, …) are superseded when the next six-month JDK ships. Do not claim a version you cannot discuss.

## LTS is what shops run; feature releases come and go

Since 9, Oracle ships a JDK about every six months. Only designated releases get Long-Term Support. On the Oracle Customer roadmap those LTS releases are **8** (GA March 2014), **11** (September 2018), **17** (September 2021), **21** (September 2023), and **25** (September 2025). Example: 9 was non-LTS and immediately superseded by 10, then 11 (LTS) kept Premier Support after 12 existed ([[How would you explain Java 17 21]], [[How would you explain notable language changes in recent Java versions]]).

Interviewers hear “I used Java 19” as “I compiled a side project.” Production answers sound like: “We ran **11** in prod until 2024, compiled with **17**, I have written **21** virtual-thread code on a service, I have not shipped **25** yet.” Tie each LTS to work: Java 8 lambdas/streams/`java.time`; 11 HTTP client / `var` (10) if you used them; 17 records/sealed; 21 virtual threads / sequenced collections / pattern `switch`; 25 only if you really did ([[What major language features arrived in Java 8]], [[How many years of Java experience do you have in total]]).

`java -version` / `Runtime.version()` (since 9) is how you check a runtime, not how you answer the question.

```d2
lts: "Oracle LTS (roadmap)" {
  shape: rectangle
  v8: "8  (2014)"
  v11: "11 (2018)"
  v17: "17 (2021)"
  v21: "21 (2023)"
  v25: "25 (2025)"
  v29: "29 planned 2027"
  v8 -> v11 -> v17 -> v21 -> v25 -> v29
}
feat: "non-LTS\n9–10, 12–16, 18–20, 22–24, 26…" {
  shape: rectangle
}
```

**Fig. 1.** Say which LTS boxes you lived in. Feature releases are not a second career unless you shipped them.

```java
String spec = System.getProperty("java.specification.version");
Runtime.Version rt = Runtime.version(); // Java 9+
```

**Listing 1.** How a process reports its JDK — useful on a ticket, not as a substitute for “we ran 17 in production.”

> [!warning] Do not invent a version résumé
>
> Listing every JDK from 6 to 25 reads as padding. Oracle JDK vs OpenJDK vs Temurin is a vendor, not extra versions. Premier/Extended Support dates are **Oracle Customer** timelines — they are not “this JDK is illegal.” Java 8 is still on that LTS list (Extended Support into 2030 on Oracle’s table). Claiming modules, records, or virtual threads without a story will be probed.

> [!tip] Interview answer
>
> **“Professionally I have shipped on Java *N* and *M* (LTS). Current prod is *X*; I have compiled against *Y*.”** Then one concrete API or language change per line. Oracle LTS today: **8, 11, 17, 21, 25**. Six-month feature releases only if you actually ran them. Honest “not yet 25” beats a fake list.
