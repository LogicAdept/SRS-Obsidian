<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #SRS

# What is `aop.xml` for load-time weaving?

> [!abstract] Short answer
> **`META-INF/aop.xml`** (or **`META-INF/aop-ajc.xml`**) is **AspectJ’s** load-time weaver config on the classpath: which **aspect types** to apply and which **target types** to weave. Spring does not invent this file. `@EnableLoadTimeWeaving`’s default **`AUTODETECT`** turns AspectJ weaving **on only if at least one such file exists**.

## What the file controls

AspectJ 5+ looks up `META-INF/aop.xml` / `META-INF/aop-ajc.xml` on the weaving class loader (including inside JARs). Several files are **merged**. Two sections:

* **`<aspects>`** — declare aspects (`<aspect name="…"/>`) or define **`<concrete-aspect>`** XML subtypes. Nested `<include>` / `<exclude>` filter **which declared aspects** run, not which application classes.
* **`<weaver>`** — weaver options (`-verbose`, `-showWeaveInfo`, …) and `<include>` / `<exclude>` **type patterns** for classes to transform. **No weaver `<include>` means every type visible to the weaver is a candidate.**

```xml
<aspectj>
	<weaver>
		<include within="com.xyz..*"/>
	</weaver>
	<aspects>
		<aspect name="com.xyz.ProfilingAspect"/>
	</aspects>
</aspectj>
```

**Listing 1.** Spring Framework 6.2’s LTW example: one `@Aspect` and a **narrow** `within` on application packages. `..*` is AspectJ “this package and subpackages.”

The aspect class must already be **compiled and on the classpath**. `aop.xml` does not compile it. Full Spring setup: [[How do you perform load-time weaving with AspectJ in a Spring application]], weaver bean: [[What is a load-time weaver in Spring]], switch: [[What is the EnableLoadTimeWeaving annotation]].

```d2
direction: down
xml: "META-INF/aop.xml" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
aspects: "aspects: which AspectJ types" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
types: "weaver include/exclude:\nwhich classes get bytecode" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
ltw: "LoadTimeWeaver adds\nClassPreProcessorAgentAdapter" {
  width: 280
  height: 55
  style.fill: "#fce4ec"
}

xml -> aspects
xml -> types
aspects -> ltw
types -> ltw
```

**Fig. 1.** Spring only registers the transformer. AspectJ reads `aop.xml` to decide **what** to weave.

`within` on `<weaver><include>` is a type pattern (AspectJ `within` PCD form; use `AND` / `OR` instead of `&&` / `||`). Too narrow: those classes load **unwoven**. Too wide: extra weave cost and AspectJ **dump files / warnings** — Spring’s LTW chapter says restrict includes to application packages.

> [!warning]Default AUTODETECT needs this file
> `@EnableLoadTimeWeaving` defaults to **`AspectJWeaving.AUTODETECT`**: if the Spring LTW infrastructure finds **no** `META-INF/aop.xml`, AspectJ weaving stays **off**. The `loadTimeWeaver` bean can still exist for JPA. **`ENABLED`** still registers the AspectJ transformer, but without declared aspects the weaver has nothing useful to apply. **`DISABLED`** skips AspectJ LTW even when `aop.xml` is present.

> [!warning]Configurable is not this XML
> `@Configurable` is acted on by **`AnnotationBeanConfigurerAspect`** in **`spring-aspects`**, which must itself be woven. XML `<context:load-time-weaver aspectj-weaving="on"/>` also turns on **`<context:spring-configured>`**. **`@EnableLoadTimeWeaving(aspectjWeaving = ENABLED)` does not** — add **`@EnableSpringConfigured`**. Do not assume a hand-written `aop.xml` listing that aspect is the documented `@Configurable` setup.

> [!tip] Interview answer
> **`aop.xml` is AspectJ’s LTW descriptor: aspects to apply and packages to rewrite.** Spring’s weaver looks for `META-INF/aop.xml` and, with the default `AUTODETECT`, enables AspectJ weaving only when that resource exists. Keep `weaver` includes tight so you do not weave the JDK or third-party JARs. The file is not a Spring AOP proxy filter and it does not replace `spring-instrument` or an instrumentable class loader.
