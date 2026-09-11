<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What was new in Java after 21

> [!abstract] Short answer
> **Post-21, the trains delivered: unnamed variables `_` (22, JEP 456), the Foreign Function & Memory API final (22, JEP 454), statements before `super()` (22 preview → 25, JEP 513), Stream Gatherers (22 preview → final 24, JEP 485), Markdown javadoc (23), synchronized without virtual-thread pinning (24, JEP 491), compact object headers (24 experimental → product 25, JEP 519), scoped values final (25, JEP 506), compact source files + `instance main` (25, JEP 512), module import declarations (25, JEP 511), Applet removal (26, JEP 504), HTTP/3 client support (26, JEP 517).** Structured concurrency kept previewing (sixth preview in 26) — still not final ([[What was new in Java 21]]).

## The release-by-release spine

**22–23:** FFM replaces JNI's unsafe core (`java.lang.foreign` final); `_` silences unused bindings; gatherers preview custom intermediate stream ops; Markdown doc comments let javadoc be written in `.md` style. **24:** gatherers final; pinning inside `synchronized` eliminated (virtual threads park, not pin); compact object headers experimental (Lilliput: 96-bit → 64-bit headers); AOT class loading/dumping (project Leyden's first user-visible steps). **25 (LTS):** the "hello-world modernization" set — compact source files with implicit classes and instance `main` (512), `import module` (511), flexible constructor bodies (513) — plus scoped values final and compact object headers product-ready; primitive patterns still previewing. **26 (March 2026):** `final`-semantics hardening groundwork (500), Applet gone (504), HTTP/3 (517), G1 synchronization reduction (522), Lazy Constants (second preview, ex-Stable Values). String templates stayed withdrawn; primitive patterns and structured concurrency remain the two big unfinished fronts ([[What is a preview feature in Java]]).

```d2
direction: right
v22: "22\nFFM final, _ vars,\ngatherers preview" {
  width: 240
  height: 75
  style.fill: "#fff8e1"
}
v23: "23\nMarkdown javadoc" {
  width: 220
  height: 60
  style.fill: "#fff8e1"
}
v24: "24\ngatherers final, no pinning,\ncompact headers experimental" {
  width: 300
  height: 75
  style.fill: "#fff3e0"
}
v25: "25 LTS\nscoped values final, compact main,\nmodule imports, pre-super, headers product" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
v26: "26\nApplet removed, HTTP/3,\nfinal-mean-final prep" {
  width: 300
  height: 75
  style.fill: "#e3f2fd"
}
v22 -> v23 -> v24 -> v25 -> v26
```

**Fig. 1.** Five trains after 21: API completions (FFM, gatherers), Loom finishing touches (no pinning, scoped values), Leyden startup work (headers, AOT), and the 25 LTS ergonomics set.

```java
// Conceptual — JDK 25+ syntax; this JDK 21 harness cannot run it.
// JEP 512 (25): an implicitly declared compact source file
void main() {
    IO.println("no class, no static, no imports ceremony");
}
// JEP 513 (25): statements before super()
// Window w = new TitleFitted("app");  // validate args, init fields pre-super
```

**Listing 1.** Conceptual (JDK 25+ only): JEP 512's implicit class runs a bare `main`, and JEP 513 allows field initialization and argument validation before the `super(...)` call — under the rule that `this` is not yet live.

> [!warning] Post-21 features in interviews: check the flag before you claim it
> The standing traps: structured concurrency is **still preview** after six rounds (25, 26) — calling it final is wrong; scoped values is the one that finalized (25). "Stream Gatherers" are final since **24**, not 21. Compact object headers need an explicit flag (`-XX:+UseCompactObjectHeaders`), not automatic in 25. And string templates are absent from this entire timeline — withdrawn, never shipped ([[What is a preview feature in Java]]).

> [!tip] Interview answer
> **After 21: FFM finalized in 22, Stream Gatherers and no-pinning virtual threads in 24, then the 25 LTS set — scoped values final, compact source files, module imports, flexible constructor bodies, compact object headers product — and 26 removed Applets and added HTTP/3.** Structured concurrency and primitive patterns are still previews; I keep final/preview straight by release, not vibes. Per-release detail: [[What was new in Java 22]], [[What was new in Java 23]], [[What was new in Java 24]], [[What was new in Java 25]].
