<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# How is JSP configured in the web deployment descriptor?

> [!abstract] Short answer
> Two `web.xml` channels. **Global:** one **`<jsp-config>`** with **`<taglib>`** maps (`taglib-uri` → `taglib-location`) and **`<jsp-property-group>`** entries (each with one or more **`url-pattern`s**). Groups mark those files as JSP and set EL, scripting, encoding, XML vs standard syntax, prelude/coda, whitespace, content type, buffer, undeclared namespaces, and (JSP 4.0) **`error-on-el-not-found`**. **Per page as a servlet:** **`<servlet>` + `<jsp-file>`** (path starts with `/`) plus mapping / init / load-on-startup — that is **not** `jsp-config`. Init params: [[How do you configure initialization parameters for a JSP]]. Descriptor: [[How would you explain the Java EE web deployment descriptor]]. Built-in tags: [[Why are built in JSP tags not configured in web.xml]]. JSP: [[What is Java Server Pages JSP]].

## `jsp-config` versus `<jsp-file>`

**`<jsp-config>`** is global JSP container setup. It has only **`taglib`** and **`jsp-property-group`**. The Servlet schema allows the `jsp-config` *element* to appear as “0 or more,” but **more than one `jsp-config` is an error**. Fragments may add **`jsp-property-group`s** (they are **additive**). Prefer **path** `url-pattern`s over `*.jsp` when the pages live in a JAR’s `META-INF/resources`.

**Taglib map.** `taglib-uri` is the URI pages use; `taglib-location` is the TLD (application-relative). Duplicate `taglib-uri` values must not appear. This **overrides** implicit TLD maps.

**Property groups.** Matching uses the same **url-pattern** syntax as servlet mappings, decided at **translation**. Matching a group makes the resource a **JSP** (implicit). Groups **do not** apply to **tag files**. Most properties apply to the **translation unit** (the page plus `include` **directive** files). **`page-encoding`** and **`is-xml`** apply **per file**.

If a resource matches both a **servlet mapping** and a **property group**, the **most specific** pattern wins. **Identical** patterns: the **servlet mapping** wins. **`include-prelude` / `include-coda`** from **every** matching group still run, in **`web.xml` order** (not “most specific only”).

Page authors can still set **`page` directive** attributes (`isELIgnored`, `pageEncoding`, `contentType`, `buffer`, `trimDirectiveWhitespaces`, …). A **different** `pageEncoding` in the directive and in a matching group is a **translation error**.

**`<jsp-file>`** lives under **`<servlet>`**. Full context path starting with `/`. That declaration gets **`init-param`**, **`load-on-startup`** (precompile), and **`servlet-mapping`**. A generic `*.jsp` mapping is a **different** servlet than a named `<jsp-file>`.

```d2
direction: down
dd: "WEB-INF/web.xml" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
cfg: "jsp-config\ntaglib + property-group" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
file: "servlet / jsp-file\nmapping + init-param" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
dd -> cfg
dd -> file
```

**Fig. 1.** Property groups configure **how pages translate**. `jsp-file` registers **one page as a servlet**.

```xml
<!-- Conceptual — jsp-configType, JSP 4.0 / web-common 6.1 -->
<jsp-config>
  <taglib>
    <taglib-uri>/tags/example</taglib-uri>
    <taglib-location>/WEB-INF/tlds/example.tld</taglib-location>
  </taglib>
  <jsp-property-group>
    <url-pattern>*.jsp</url-pattern>
    <scripting-invalid>true</scripting-invalid>
    <trim-directive-whitespaces>true</trim-directive-whitespaces>
    <error-on-undeclared-namespace>true</error-on-undeclared-namespace>
  </jsp-property-group>
</jsp-config>
```

**Listing 1.** `scripting-invalid` makes scriptlets a **translation error**. EL stays on for Servlet 2.4+ `web.xml` unless `el-ignored` is true.

```xml
<servlet>
  <servlet-name>report</servlet-name>
  <jsp-file>/WEB-INF/report.jsp</jsp-file>
  <load-on-startup>1</load-on-startup>
</servlet>
```

**Listing 2.** Not a property group: this page is a named servlet (init params and mapping go here).

> [!warning] Property groups are not servlet init
> `${initParam}` is **context-param**. Per-page init is **`<jsp-file>` + `<init-param>`**. `el-ignored` / `scripting-invalid` do **not** apply to tag files the same way; tag files default to **evaluating EL**. Unknown namespaces on standard-syntax pages are **ignored** unless `error-on-undeclared-namespace` is true.

> [!warning] Prelude order is document order
> Matching `/two/*.jsp` plus `*.jsp` **stacks** preludes/codas from **both** groups in descriptor order. `is-xml` true treats the group as **JSP documents**. `trim-directive-whitespaces` does **nothing** on XML syntax.

> [!tip] Interview answer
> In web.xml I use one jsp-config: taglib maps for TLDs, and jsp-property-group url-patterns for encoding, EL, scripting, and automatic prelude include. That is separate from declaring a page with jsp-file under servlet, which is how I attach init-param and load-on-startup. Page directives can override some of those defaults, but a conflicting pageEncoding is a translation error.
