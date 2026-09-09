<!--
reps: 0
priority: 0
-->
#Java/Library #SRS

# What approaches exist for writing or generating XML in Java?

> [!abstract] Short answer
> **Four practical paths: build a DOM and serialize it with a `Transformer`; write streaming with a StAX `XMLStreamWriter`; run XSLT through `Transformer` over any `Source`; or marshal objects with JAXB — which left the JDK in Java 11 and now lives in the `jakarta.xml.bind` artifact.** SAX has no writer: it is read-only by design.

## Build a tree, then serialize

The DOM route constructs an `org.w3c.dom.Document` with `DocumentBuilder.newDocument()`, attaches elements and attributes, then hands the tree to a `Transformer` (`DOMSource` → `StreamResult`). The same `Transformer` serializes any source, and its `OutputKeys` — `INDENT`, `ENCODING`, `OMIT_XML_DECLARATION` — control formatting. This is the natural choice when you already hold the data as a tree or need to modify before writing ([[How would you explain JAXP for XML parsing and transformation in Java]]).

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

**Listing 1.** Verified on JDK 21: a DOM built in memory and serialized by `Transformer` with indentation.

## Write streaming, or map objects

The StAX route never builds a tree: `XMLOutputFactory.createXMLStreamWriter(...)` hands you a cursor API — `writeStartDocument`, `writeStartElement`, `writeAttribute`, `writeCharacters`, `writeEndDocument` — emitting well-formed markup element by element, memory-flat for huge outputs. The XSLT route treats generation as transformation: feed any `Source` (DOM, SAX events, StAX stream, or a file) with a stylesheet. JAXB is the object-mapping route: annotate classes, `Marshaller.marshal(...)`; since Java 11 it is not in the JDK — add `jakarta.xml.bind` explicitly ([[When should you use DOM versus SAX or StAX]]).

```java
StringWriter sink = new StringWriter();
XMLOutputFactory outF = XMLOutputFactory.newInstance();
XMLStreamWriter w = outF.createXMLStreamWriter(sink);
w.writeStartDocument();
w.writeStartElement("item");
w.writeAttribute("sku", "A-1");
w.writeCharacters("Keyboard");
w.writeEndElement();
w.writeEndDocument();
w.flush();
System.out.println("written: " + sink);
// written: <?xml version="1.0" ?><item sku="A-1">Keyboard</item>
```

**Listing 2.** Verified on JDK 21: `XMLStreamWriter` emits the declaration, attributes, and escaped text in a single pass.

> [!warning] Never assemble XML by string concatenation
> Concatenating `"<item>" + value + "</item>"` breaks the moment the value contains `<`, `&`, or a quote — the output is malformed or injects foreign elements, and the encoding is whatever the writer guessed. The API writers escape text and attribute values and declare the encoding for you. Second trap: a `Transformer` without `OutputKeys.INDENT` writes the whole document on one line, which people then misdiagnose as a bug in their DOM ([[How would you explain JSON vs XML]]).

```d2
direction: right
d1: "DOM tree\nDocument -> appendChild" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
d2: "StAX cursor\nXMLStreamWriter" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
d3: "JAXB marshal\nobjects -> XML" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
out: "Transformer\nSource -> Result" {
  width: 220
  height: 70
  style.fill: "#fff8e1"
}
d1 -> out
d2 -> out
d3 -> out
```

**Fig. 1.** All generation paths converge on a `Transformer`-style serialization or produce markup directly through the StAX writer.

> [!tip] Interview answer
> **Build a DOM and serialize with `Transformer` when you need a tree; stream with `XMLStreamWriter` for flat-memory generation; run XSLT for document-shaped transformations; marshal with JAXB — since Java 11 an external `jakarta.xml.bind` dependency, not JDK.** SAX cannot write. And never concatenate XML strings: the APIs handle escaping and encoding, concatenation handles neither.

> [!example] Verified behavior
> JDK 21: DOM build + `Transformer` with `INDENT` produced a two-line indented document; `XMLStreamWriter` emitted `<?xml version="1.0" ?><item sku="A-1">Keyboard</item>`; an XSLT stylesheet over a two-item source rendered an HTML fragment.
