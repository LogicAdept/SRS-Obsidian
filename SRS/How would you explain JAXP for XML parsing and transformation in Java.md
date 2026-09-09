<!--
reps: 0
priority: 0
-->
#Java/Library/JAXP #SRS

# How would you explain JAXP for XML parsing and transformation in Java?

> [!abstract] Short answer
> **JAXP is the JDK's umbrella API for XML processing: DOM, SAX, and StAX parsing plus XSLT transformation, all behind pluggable factory interfaces.** It ships inside the JDK in the `java.xml` module — no dependency needed — and lets you swap parser implementations without touching calling code.

## One API, three parsing styles, one transformer

JAXP (Java API for XML Processing) organizes XML work by style. **DOM** — `javax.xml.parsers.DocumentBuilderFactory` → `DocumentBuilder` → an in-memory `org.w3c.dom.Document` tree. **SAX** — `javax.xml.parsers.SAXParserFactory` → `SAXParser` pushing events into your `DefaultHandler` callbacks. **StAX** — `javax.xml.stream.XMLInputFactory` → `XMLStreamReader` pulled event by event (since Java 6, also `XMLOutputFactory`/`XMLStreamWriter` for writing). **Transformation** — `javax.xml.transform.TransformerFactory` → `Transformer` (the TrAX API), which runs XSLT or copies any `Source` to any `Result` ([[When should you use DOM versus SAX or StAX]]).

The pluggability is the point: every entry point is an abstract factory. `newInstance()` looks up an implementation via system properties, then `ServiceLoader`, then a JDK default (an Xerces-derived parser). Application code depends on the API, so a different parser can be dropped in.

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.newDocument();

Element root = doc.createElement("order");
root.setAttribute("id", "42");
doc.appendChild(root);
Element item = doc.createElement("item");
item.setAttribute("sku", "A-1");
item.setTextContent("Keyboard");
root.appendChild(item);

Transformer t = TransformerFactory.newInstance().newTransformer();
t.setOutputProperty(OutputKeys.INDENT, "yes");
t.transform(new DOMSource(doc), new StreamResult(System.out));
// <?xml version="1.0" encoding="UTF-8" standalone="no"?>
// <order id="42">
//     <item sku="A-1">Keyboard</item>
// </order>
```

**Listing 1.** Verified on JDK 21: build a DOM, then a `Transformer` serializes it — JAXP covers both the model and the writing path ([[What approaches exist for writing or generating XML in Java]]).

```d2
direction: down
api: "JAXP factory APIs\njavax.xml.parsers / javax.xml.stream / javax.xml.transform" {
  width: 430
  height: 80
  style.fill: "#e3f2fd"
}
impl: "Implementation lookup\nsystem property -> ServiceLoader -> JDK default" {
  width: 420
  height: 80
  style.fill: "#fff3e0"
}
eng: "Parser engine (Xerces-derived) + XSLT engine\ninside the java.xml module" {
  width: 400
  height: 80
  style.fill: "#e8f5e9"
}
api -> impl -> eng
```

**Fig. 1.** Your code talks to factories; the JDK resolves which engine actually parses or transforms.

> [!warning] The default parser resolves external entities — that is an XXE hole
> A `DocumentBuilderFactory` or `SAXParserFactory` with default features will fetch external DTDs and entities from whatever the document names, turning untrusted XML into a file-read or SSRF vector. Hardening means setting features explicitly — `disallow-doctype-decl` to `true`, or both external-entity features to `false` — per factory instance. The second trap is configuration drift: because `newInstance()` honors system properties and the service loader, the "same" factory can resolve to a different engine on another classpath, changing behavior ([[How does well-formed XML differ from valid XML]], [[How would you explain XML DTD]]).

> [!tip] Interview answer
> **JAXP is the standard XML API bundled in the JDK: DOM, SAX, and StAX parsing plus XSLT transformation through factory interfaces in `javax.xml.*`.** Each style has its factory — `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `TransformerFactory` — and the implementation is pluggable, with an Xerces-derived default inside `java.xml`. For untrusted XML, lock down entity resolution features before parsing, or you have an XXE exposure.

> [!example] Verified behavior
> On plain JDK 21 (no external jars): DOM built and serialized with indented output, then parsed back — `root=order id=42`, item text `Keyboard`; SAX counted 3 elements and 2 attributes from push callbacks; StAX pulled events and wrote `<item sku="A-1">Keyboard</item>`; XSLT produced an HTML fragment from a 2-item source.
