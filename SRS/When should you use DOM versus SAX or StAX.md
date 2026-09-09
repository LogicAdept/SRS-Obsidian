<!--
reps: 0
priority: 0
-->
#Java/Library #SRS

# When should you use DOM versus SAX or StAX?

> [!abstract] Short answer
> **DOM when the document fits in memory and you need random access or modification; SAX for fast, read-only, push-style streaming of large inputs; StAX when you want streaming memory cost but a pull-style loop you control — and the ability to write XML too.** All three ship in the JDK under JAXP.

## Three mental models

**DOM** parses the whole document into a tree of `Node` objects held in memory. You can traverse, revisit, modify, and then serialize it — that flexibility costs memory roughly proportional to the document size, several times the raw text. **SAX** is push: the parser drives, calling your `DefaultHandler` callbacks — `startElement`, `characters`, `endElement` — as it reads; you keep the state, you cannot go back, memory stays flat. **StAX** is pull: you call `XMLStreamReader.next()` in your own loop and get an event code — `START_ELEMENT`, `CHARACTERS`, `END_ELEMENT`; you keep the cursor's position instead of bookkeeping parser state, and the same `javax.xml.stream` package provides `XMLStreamWriter` for writing ([[How would you explain JAXP for XML parsing and transformation in Java]]).

```java
XMLInputFactory in = XMLInputFactory.newInstance();
XMLStreamReader r = in.createXMLStreamReader(new StringReader(xml));
while (r.hasNext()) {
    int ev = r.next();                       // you pull: the loop is yours
    switch (ev) {
        case XMLStreamConstants.START_ELEMENT ->
                System.out.println("START " + r.getLocalName());
        case XMLStreamConstants.CHARACTERS ->
                System.out.println("TEXT '" + r.getText().trim() + "'");
        case XMLStreamConstants.END_ELEMENT ->
                System.out.println("END " + r.getLocalName());
        case XMLStreamConstants.END_DOCUMENT -> System.out.println("DONE");
        default -> { }
    }
}
r.close();
// START inventory / TEXT '' / START item / TEXT 'Keyboard'
// / END item / TEXT '' / END inventory / DONE
```

**Listing 1.** Verified on JDK 21: a StAX pull loop. Note the whitespace `TEXT ''` events between elements — real data arrives exactly as the file stores it.

The SAX version of the same parse inverts control: you register a `DefaultHandler` and the parser *pushes* `start: inventory`, `start: item attrs=1`, `text: Keyboard`... into your callbacks, counting state as it goes.

> [!warning] Streaming does not mean "no memory concerns at all"
> DOM on a multi-gigabyte input dies with `OutOfMemoryError` long before parsing finishes — that is the classic failure. But SAX/StAX bring their own traps: inter-element whitespace arrives as `CHARACTERS`/text nodes, so untrimmed text handling corrupts content; the `xml:space`-style details and entity boundaries can split one logical text across several callback events; and you cannot revisit an element you already passed — if the task needs look-ahead or joins across the document, streaming forces you into a second pass or a hand-built index, and DOM would have been simpler ([[How does well-formed XML differ from valid XML]]).

```d2
direction: down
doc: "XML input" {
  width: 180
  height: 50
  style.fill: "#fff8e1"
}
dom: "DOM\ntree in memory\nrandom access, modify" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
sax: "SAX\nparser pushes to callbacks\nread-only, flat memory" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
stax: "StAX\nyou pull event by event\nread + write, flat memory" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
doc -> dom
doc -> sax
doc -> stax
```

**Fig. 1.** Same input, three contracts: a tree you own, events pushed at you, events you pull.

> [!tip] Interview answer
> **Pick by access pattern: DOM for small-to-medium documents needing navigation, modification, or serialization; SAX for one-pass, read-only scanning where the parser pushes callbacks and memory stays flat; StAX when you want streaming cost with a pull loop you control — plus it is the only one of the three that also writes XML.** Watch for whitespace text events in streams, and never feed a giant document to DOM.

> [!example] Verified behavior
> JDK 21: the StAX loop printed `START inventory`, `TEXT ''` (whitespace), `START item`, `TEXT 'Keyboard'`, `END item`...; the SAX handler counted 3 elements and 2 attributes from pushed callbacks; the same file as DOM would hold every node in memory.
