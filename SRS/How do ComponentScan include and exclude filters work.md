<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS

# How do `@ComponentScan` include and exclude filters work?

> [!abstract] Short answer
> They are `TypeFilter`s on the classpath scanner. A class in the base packages becomes a candidate only if it matches **at least one include** filter and **no exclude** filter. Default includes are stereotype `@Component` (and meta-annotations such as `@Service`). Extra `includeFilters` **add** types, even without `@Component`. `excludeFilters` always win. `useDefaultFilters = false` drops the stereotype includes so only your include list remains.

## Default includes, then your filters

With `useDefaultFilters = true` (the default), the scanner registers an `AnnotationTypeFilter` for `@Component`. That also matches types meta-annotated with `@Component` — `@Repository`, `@Service`, `@Controller`, `@Configuration`, `@RestController`, and your own composed stereotypes. If Jakarta Inject is on the classpath, `@Named` is registered as another default include.

You then add `includeFilters` / `excludeFilters` on `@ComponentScan`, or `<context:include-filter>` / `<context:exclude-filter>` under `<context:component-scan>`.

```java
@Configuration
@ComponentScan(
        basePackages = "org.example",
        includeFilters = @ComponentScan.Filter(
                type = FilterType.REGEX, pattern = ".*Stub.*Repository"),
        excludeFilters = @ComponentScan.Filter(Repository.class))
public class AppConfig {
}
```

**Listing 1.** Conceptual Java: extra include for stub repository class names; exclude every `@Repository`. `@Filter(Repository.class)` defaults to `FilterType.ANNOTATION`.

```xml
<context:component-scan base-package="org.example">
    <context:include-filter type="regex"
            expression=".*Stub.*Repository"/>
    <context:exclude-filter type="annotation"
            expression="org.springframework.stereotype.Repository"/>
</context:component-scan>
```

**Listing 2.** Equivalent XML. Each filter needs `type` and `expression`.

`includeFilters` are **in addition to** the default filters. A type that matches an include is registered even if it is not annotated with `@Component`. That is why `useDefaultFilters = false` is the usual partner when the include list should be the **only** way in.

## Filter types

| `FilterType` / XML `type` | What you pass | Match |
|---|---|---|
| `ANNOTATION` (default) | annotation class / FQCN | annotation present or **meta-present** at type level |
| `ASSIGNABLE_TYPE` | class or interface | target is assignable to that type |
| `ASPECTJ` | AspectJ type pattern | e.g. `org.example..*Service+` |
| `REGEX` | regex | fully-qualified **class name** |
| `CUSTOM` | `TypeFilter` implementation | your `match(MetadataReader, …)` |

On `@ComponentScan.Filter`, `classes` / `value` is the annotation, assignable type, or `TypeFilter`, depending on `type`. `pattern` is for `ASPECTJ` and `REGEX`. Several classes on one filter are **OR**. Several include filters are also OR: one hit is enough.

```d2
direction: down
pkg: "Classes under basePackages" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
ex: "Any exclude filter match?\n→ drop" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
inc: "Any include filter match?\n(defaults ∪ includeFilters)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ok: "Candidate bean definition\n(concrete type, @Conditional ok)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
drop: "Skip" {
  width: 140
  height: 50
  style.fill: "#ffebee"
}

pkg -> ex
ex -> drop: yes
ex -> inc: no
inc -> ok: yes
inc -> drop: no
```

**Fig. 1.** `ClassPathScanningCandidateComponentProvider.isCandidateComponent`: excludes first, then at least one include. `@Conditional` is evaluated only after an include hit.

The scanner is ASM-backed (`MetadataReader`). After a class passes the filters, a second check keeps **concrete** top-level types (not interfaces or enclosing-class dependents), unless the type declares `@Lookup` methods. See [[What is the Spring ComponentScan annotation]] and [[What is the difference between Component and ComponentScan]].

> [!warning] Include does not override exclude
> If a class matches both an include and an exclude, it is **out**. The official match rule is: no exclude, and at least one include.

> [!warning] `useDefaultFilters = false` is not optional decoration
> Leaving defaults on and adding `ASSIGNABLE_TYPE` includes **both** stereotypes **and** that type. To scan “only implementations of `PaymentGateway`,” set `useDefaultFilters = false` and an assignable include. Otherwise every `@Service` in the package still comes in.

> [!warning] `@ComponentScan` has no `annotation-config` switch
> XML `<context:component-scan>` also enables `<context:annotation-config>` (`AutowiredAnnotationBeanPostProcessor`, `CommonAnnotationBeanPostProcessor`). You can set `annotation-config="false"` on the XML element. `@ComponentScan` has **no** such attribute: annotation-config processing is assumed. On `AnnotationConfigApplicationContext`, those processors are **always** registered; a hypothetical disable on `@ComponentScan` would be ignored.

> [!warning] Regex and AspectJ skip the component index
> Indexed include filters (`AnnotationTypeFilter` / `AssignableTypeFilter` for `@Indexed` types) can use Spring’s component index. Any other include filter type forces a full classpath scan.

> [!tip] Interview answer
> Include and exclude filters are TypeFilters on component scan. Defaults already include @Component and its stereotypes. Extra includes add types even without @Component; excludes run first and always win. Set useDefaultFilters to false when the include list should be the only door. XML can turn off annotation-config; @ComponentScan cannot.
