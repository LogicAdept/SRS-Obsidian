<!--
reps: 0
priority: 0
-->
#Java/Testing/Mockito #SRS

# How would you explain verify

> [!abstract] Short answer
> **`verify` is the Mockito step that checks how a mock was used: which method, with which arguments, how many times.** It never calls real code and never checks state — it inspects the mock's recorded invocations against a mode like `times(1)`, `never()`, or `atLeastOnce()`.

## What verification checks

Mocking splits a test in two: stubbing (`when`) prepares answers, verification (`verify`) confirms interactions. A mock records every invocation in a journal; `verify` replays the check against that journal. `times(1)` is the default, so `verify(mock).add("once")` and `verify(mock, times(1)).add("once")` are the same check.

```d2
direction: right
calls: "Calls on the mock\nduring the test" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
journal: "Mock's internal\ninvocation journal" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
mode: "Mode picks the rule:\ntimes / never / atLeast / atMost" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
match: "Argument matchers filter\nwhich invocations count" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
ok: "Matched count satisfies\nthe mode -> pass" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
fail: "Otherwise ->\nVerification failure" {
  width: 250
  height: 80
  style.fill: "#ffebee"
}
calls -> journal
journal -> match
mode -> match
match -> ok
match -> fail
```

**Fig. 1.** Verification is a query over recorded invocations, filtered by arguments and judged by a counting mode.

```java
List<String> mockedList = mock(List.class);
mockedList.add("once");
mockedList.add("twice");
mockedList.add("twice");

verify(mockedList).add("once");                    // times(1) is the default
verify(mockedList, times(2)).add("twice");
verify(mockedList, never()).add("never happened"); // never() == times(0)
verify(mockedList, atLeastOnce()).add("once");
verify(mockedList, atMost(5)).add("twice");
System.out.println("all verifications passed");
```

**Listing 1.** The counting modes on a mocked `List`. Run on JDK 21 with Mockito 5.11, it prints `all verifications passed`.

## When verification fails

The mode decides what counts as a violation. Expecting `times(4)` where the mock saw 2 calls throws `TooFewActualInvocations`; calling a method that was stubbed to throw would surface under `never()`. The message shows both sides — wanted versus actual — which is why over-specific verification produces noisy failures.

```java
verify(mockedList, times(4)).add("twice");
// TooFewActualInvocations:
// list.add("twice");
// Wanted 4 times:
//    -> at VerifyDemo.main(...)
// But was 2 times:
//    -> at VerifyDemo.main(...)
```

**Listing 2.** A failing verification names the method, the wanted count, and where the real calls happened.

> [!warning] Verifying everything makes tests brittle
> A common interview trap is treating `verify` as the main assertion tool. State checks (`assertEquals` on results) usually localize defects better; interaction checks are for behavior that IS the contract — "the email was sent", "the repository was saved exactly once". Over-verification (checking every intermediate call) pins the implementation instead of the outcome and breaks on harmless refactors. Also remember verification ignores actual return values — a stubbed answer passing through does not make a wrong interaction correct. Combine with [[Which assertions does JUnit provide]] for state and [[How would you explain ArgumentCaptor]] when the exact argument values matter.

## Verify vs the Spring layer

In plain unit tests `verify` is the only interaction tool. In Spring tests the same idea is wrapped by `@MockBean`/`@SpyBean`-style helpers — see [[What is the difference between Mock and MockBean]] and [[What is SpyBean]] for how the Spring context replaces beans while keeping Mockito's verification API on top.

> [!tip] Interview answer
> **`verify` checks interactions with a mock: it replays the mock's recorded invocations and compares them against a counting mode — `times`, `never`, `atLeast`, `atMost` — with `times(1)` as the default. Arguments are matched with the same matchers as stubbing. It is an interaction assertion, not a state assertion, so use it for side-effect contracts like "save was called exactly once", not for everything.**

