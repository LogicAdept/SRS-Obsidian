<!--
reps: 0
priority: 0
-->
#Java/JSP/Tags #SRS

# How can you extend JSP functionality?

> [!abstract] Short answer
> **With a tag library.** That is the JSP **tag extension** mechanism: new **custom actions**, **EL functions**, optional **listeners**, and **translation-time validators**, described by a **TLD** and imported with **`<%@ taglib %>`**. Handlers are **Java** (`Tag` / `IterationTag` / `BodyTag` or `SimpleTag`) or **tag files** (`.tag` / `.tagx`). **JavaBeans** encapsulate data on the same page (`jsp:useBean`); they do **not** add tags. Standard `jsp:` actions are **not** an extension you register. Built-in vs custom: [[Why are built in JSP tags not configured in web.xml]]. Authoring: [[What do you know about authoring custom JSP tags]].

## Tag libraries, then beans

Jakarta Pages **4.0** names two ways to **encapsulate** functionality: **JavaBeans** and **tag libraries** (custom actions, functions, listener classes, validation). **Extending the set of tags the container understands** is the library path. New actions follow Chapter **7** (`jakarta.servlet.jsp.tagext`) and enter a page through **`taglib`**. JSTL is one such library, not a second language: [[How would you explain JSTL the JSP Standard Tag Library]]. Descriptor URI maps: [[How is JSP configured in the web deployment descriptor]].

**Import.** `<%@ taglib prefix="ex" uri="…" %>` binds a prefix to a TLD. **`tagdir="/WEB-INF/tags/…"`** uses an implicit TLD for tag files; it must start with `/WEB-INF/tags`, the directory must exist, and it **cannot** appear with `uri`. Prefixes `jsp:`, `jspx:`, `java:`, `jakarta:`, and `servlet:` are **reserved**. Unknown `prefix:Name` is a translation error. Missing TLD path is fatal. `taglib` must appear **before** any action that uses that prefix.

**Java handlers.** **Classic** (JSP 1.2 style): `Tag`, `IterationTag` (`doAfterBody`), `BodyTag` (`BodyContent`). Optional mix-in `TryCatchFinally`. Base classes `TagSupport` / `BodyTagSupport`. The container **may reuse** a classic instance. **Simple** (JSP 2.0+): `SimpleTag` / `SimpleTagSupport`, lifecycle **construct → inject → set properties → `doTag` → discard** — **do not cache**. Body is a `JspFragment` (`setJspBody`); `body-content` **`JSP` is illegal** for SimpleTag. `SkipPageException` skips the rest of the page. `DynamicAttributes` for extra names. Classic nested in SimpleTag needs `TagAdapter`.

**Tag files.** Page-author extensions in JSP syntax (no Java required). Extension **`.tag` / `.tagx`**. Live in **`/WEB-INF/tags/`** (or a subdir) or **`META-INF/tags/`** inside a JAR in `WEB-INF/lib`. Anywhere else the container **does not** treat them as tags (a file in the docroot is just content). `jsp:invoke` / `jsp:doBody` exist **only** in tag files.

**Also in a TLD.** **Functions:** EL `prefix:name(…)` → **public static** method; unique function name per library. **`listener`** classes are registered like `web.xml` listeners (order undefined, before application start). **`TagLibraryValidator`** / **`TagExtraInfo`** validate the XML view at translation time.

**Not this mechanism.** `<%@ page extends="…" %>` names the servlet **superclass** and blocks container-specialized bases — not a tag library. Scriptlets glue one page; they do not add portable actions.

```d2
direction: down
page: "JSP page\n<%@ taglib prefix uri|tagdir %>" {
  width: 300
  height: 48
  style.fill: "#fff8e1"
}
tld: "TLD\nactions · functions · listeners" {
  width: 300
  height: 48
  style.fill: "#e8f5e9"
}
h: "Tag / SimpleTag class\nor .tag file" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
page -> tld: "URI or tagdir"
tld -> h: "translation + request"
```

**Fig. 1.** Extending JSP means **importing a library**, not subclassing the generated servlet.

```java
// Conceptual — Jakarta Pages 4.0 SimpleTag
public class HelloTag extends SimpleTagSupport {
    private String name;
    public void setName(String name) { this.name = name; }

    @Override
    public void doTag() throws JspException, IOException {
        getJspContext().getOut().write("Hello, " + name);
    }
}
```

**Listing 1.** Simple tag handler. The TLD names `HelloTag` and the action `hello`. The container must **not** reuse this instance.

```jsp
<%-- Conceptual — /WEB-INF/tags/hello.tag --%>
<%@ attribute name="name" required="true" %>
Hello, ${name}
```

```jsp
<%-- Conceptual — consuming page --%>
<%@ taglib prefix="t" tagdir="/WEB-INF/tags" %>
<%@ taglib prefix="ex" uri="/tags/hello" %>
<t:hello name="tag file" />
<ex:hello name="${user}" />
${ex:upper("el function")}
```

**Listing 2.** Tag file via `tagdir`, Java tag via `uri`, EL function from the same TLD style map. `jsp:useBean` can still hold the `user` bean; that is **data**, not a new tag.

> [!warning] `tagdir` and `uri` together, or a reserved prefix, fail translation
> `tagdir` must be an existing `/WEB-INF/tags…` directory. A `.tag` outside those trees is **not** a tag. If the URI cannot be resolved to **one** TLD path, translation fails. Standard `jsp:include` / `jsp:useBean` are **not** listed in your TLD.

> [!warning] Classic handlers may be reused; SimpleTag must not
> Do not keep request-specific fields on a **classic** `Tag` after the invocation. `SimpleTag` is one-shot. `SimpleTag` + TLD `body-content` of `JSP` is an **invalid page**. Resource injection applies to Java tag handlers and TLD listeners, **not** to JSP pages or tag files.

> [!tip] Interview answer
> I extend JSP with a tag library: a TLD plus custom actions, imported with taglib. Handlers are Java Tag or SimpleTag classes, or tag files under WEB-INF/tags. The same TLD can expose EL functions and listeners. Beans encapsulate objects on the page; they do not add new tags, and page extends is not how you grow the tag set.
