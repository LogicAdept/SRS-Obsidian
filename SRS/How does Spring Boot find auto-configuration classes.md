<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# How does Spring Boot find auto-configuration classes?

> [!abstract] Short answer
> `@EnableAutoConfiguration` (inside `@SpringBootApplication`) imports **`AutoConfigurationImportSelector`**, a **`DeferredImportSelector`**. Candidates are **not** component-scanned: Boot loads fully qualified class names from every jar’s **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (one type per line) via **`ImportCandidates`**. Each class is still a `@Configuration` (`@AutoConfiguration`) gated by **`@Conditional`**.

## Imports file, then conditions

Boot 4 locates auto-configuration with **`ImportCandidates`**, not `SpringFactoriesLoader` for this key. Put the file in the **published** jar (typically a starter’s auto-config module):

```
com.mycorp.libx.autoconfigure.LibXAutoConfiguration
com.mycorp.libx.autoconfigure.LibXWebAutoConfiguration
```

**Listing 1.** Official layout: one FQCN per line. `#` starts a comment. A nested type must use `$` (`com.example.Outer$NestedAutoConfiguration`). List only the **replacement** class if you also ship `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.replacements`.

`@AutoConfiguration` is `@Configuration`. Order uses `before` / `after` (or `@AutoConfigureBefore` / `@AutoConfigureAfter` / `@AutoConfigureOrder`) — that orders **bean definitions**, not creation. Conditions still decide whether the class actually applies ([[How do ConditionalOn annotations drive auto-configuration]]). Confirm with the conditions report ([[How can you debug which auto-configuration classes applied]]).

```d2
direction: right
jars: "JARs on the classpath" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
file: "AutoConfiguration.imports\none FQCN per line" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
sel: "AutoConfigurationImportSelector\nDeferredImportSelector" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
cfg: "@AutoConfiguration\nthen @Conditional" {
  width: 200
  height: 70
  style.fill: "#f3e5f5"
}

jars -> file -> sel -> cfg
```

**Fig. 1.** `@SpringBootApplication` enables auto-config; the selector reads **every** matching imports file, then exclusions (`exclude` / `spring.autoconfigure.exclude`) drop names before conditions run ([[How do you disable a specific auto-configuration class]]).

Boot 2.x registered the same types in **`META-INF/spring.factories`** under **`org.springframework.boot.autoconfigure.EnableAutoConfiguration`**. **2.7** added the `.imports` file and still honored `spring.factories`. **3.0** **removed** that key; other `spring.factories` keys (`ApplicationListener`, and so on) are unchanged. A library that must support 2.7 and 3.x lists **both** files (2.7 de-duplicates).

> [!warning] `spring.factories` is not auto-config on Boot 3+
> A custom starter that **only** lists `EnableAutoConfiguration` in `spring.factories` is **not** loaded. There is **no** fail-fast for that miss. Other `spring.factories` entries still work — do not delete the whole file if you still register listeners or initializers.

> [!warning] Do not component-scan auto-config
> Official rule: load auto-configurations **only** by naming them in the imports file. Keep them out of a scanned package, and do **not** put `@ComponentScan` on the auto-config class (use `@Import`). A class annotated `@AutoConfiguration` but missing from `.imports` is invisible. Naming in `.imports` **and** scanning it registers it twice.

> [!tip] Interview answer
> Boot finds auto-config by reading META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports from each jar, one class name per line, because @EnableAutoConfiguration imports AutoConfigurationImportSelector. That replaced the EnableAutoConfiguration key in spring.factories, which Boot 3 no longer reads. The listed classes are still @Conditional @Configuration, not something component scan is supposed to pick up.
