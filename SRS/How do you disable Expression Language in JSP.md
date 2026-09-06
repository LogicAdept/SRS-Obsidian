<!--
reps: 0
priority: 0
-->
#Java/JSP/EL #Java/Servlet #SRS

# How do you disable Expression Language in JSP?

> [!abstract] Short answer
> **Set `isELIgnored="true"` on the page (or `tag` on a tag file), or `<el-ignored>true</el-ignored>` in a matching `jsp-property-group`.** Ignored `${…}` / `#{…}` are copied **verbatim**. The **page directive wins** over the group. Tag files **always evaluate** unless the **tag** directive says otherwise — `web.xml` has **no** `el-ignored` for them. This is not `scripting-invalid` and not `error-on-el-not-found`. Groups: [[How is JSP configured in the web deployment descriptor]]. EL itself: [[What do you know about the JSP Expression Language]].

## Page directive, then the property group

Jakarta Pages **4.0** §3.3.2: each JSP has a default for whether EL is **ignored** (passed through) or **evaluated**. `${expr}` was unreserved before JSP **2.0**, `#{expr}` before **2.1**.

**Default for pages** follows the **`web.xml` schema version**: Servlet **2.3 or earlier** → ignore (compatibility). Servlet **2.4 or later** (including Jakarta Servlet **6.x**) → evaluate `${}`. `#{…}` evaluation starts at JSP **2.1**. **Tag files** ignore that default and **evaluate** unless told otherwise.

**Override, two places:**

1. **`<%@ page isELIgnored="true" %>`** — this page and its **translation unit** (`include` **directive** files). `false` recognizes `${…}` and `#{…}` in template text and action attributes.
2. **`<jsp-property-group><el-ignored>true</el-ignored>`** — matching `url-pattern`s. Valid values `true` / `false`.

**Table JSP.3-1 (pages):** if the directive is unspecified, the group (or the web.xml-version default) applies. If the directive is **`true` or `false`**, that value is used (**`don’t care`** what the group says). **Table JSP.3-2 (tag files):** unspecified / `false` → evaluated; `true` → ignored. The tag directive’s `isELIgnored` has **no** matching `web.xml` element.

When EL is **on**, `\$` and `\#` quote `$` / `#` in template text and attributes. When EL is **off**, those sequences are **not** quotes (`\$` is two characters). In JSP documents, XML attribute `\\` is not an escape the same way as standard syntax. Quoting without disabling: [[Can you use JavaScript inside a JSP page]]. JSP: [[What is Java Server Pages JSP]].

A **`tagdependent`** action body also skips EL; that is per-tag body content, not a page switch. `deferredSyntaxAllowedAsLiteral` only lets `#{` appear as a string literal. `errorOnELNotFound` / `error-on-el-not-found` still **run** EL; they change missing-identifier behavior.

```d2
direction: down
dir: "page / tag isELIgnored" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
grp: "jsp-property-group el-ignored\n(pages only)" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
def: "web.xml ≤ 2.3 ignore\n≥ 2.4 evaluate\ntag files: evaluate" {
  width: 280
  height: 64
  style.fill: "#e3f2fd"
}
dir -> grp: "unspecified"
grp -> def: "unspecified"
```

**Fig. 1.** Directive first, then property group, then the version default. Tag files never consult `el-ignored`.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<%@ page isELIgnored="true" %>
<p>${user.name}</p>
```

**Listing 1.** The characters `${user.name}` are written to `out` as template text. With `isELIgnored="false"` (or a 2.4+ app and no override), the container would evaluate the expression.

```xml
<!-- Conceptual — jsp-property-group, JSP 4.0 -->
<jsp-config>
  <jsp-property-group>
    <url-pattern>*.jsp</url-pattern>
    <el-ignored>true</el-ignored>
  </jsp-property-group>
</jsp-config>
```

**Listing 2.** Group-level off switch for matching pages. A page with `isELIgnored="false"` **still evaluates**. Tag files under `/WEB-INF/tags` are **unaffected**.

```jsp
<%-- Conceptual — tag file; no web.xml default --%>
<%@ tag isELIgnored="true" %>
```

**Listing 3.** Only way to ignore EL in a tag file.

> [!warning] `scripting-invalid` does not turn off EL
> It bans `<%` / `<%!` / `<%=`, not `${`. `el-ignored` does not apply to **tag files**; they keep evaluating until `<%@ tag isELIgnored="true" %>`. A modern `web.xml` (2.4+) **evaluates** EL unless you set a group or the page directive.

> [!warning] The page directive beats the property group
> `isELIgnored="true"` ignores EL even if `el-ignored` is `false`. `isELIgnored="false"` evaluates even if the group says ignore. With EL off, do not write `\$` expecting a quoted `$` — that quote exists **only** when EL is on. `error-on-el-not-found` is a different switch.

> [!tip] Interview answer
> I disable EL with `isELIgnored="true"` on the page, or `el-ignored` in a JSP property group. The page directive overrides the group. Tag files always evaluate EL unless the tag directive says otherwise, and web.xml cannot change that. A Servlet 2.3 descriptor ignored EL by default; 2.4 and later evaluate it.
