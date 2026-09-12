<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is DOCTYPE and why is it needed?

> [!abstract] Short answer
> **`<!DOCTYPE html>` is the required preamble of an HTML document; the HTML standard calls it a "required header".** It is not an element or a tag - it is an instruction that switches the browser into standards-compliant rendering. Without a doctype the page renders in **quirks mode**, where layout emulates the behavior of old Navigator 4 and Internet Explorer 5 engines and deviates from modern CSS specifications.

## What the doctype actually controls

Browsers have three rendering modes: **no-quirks**, **limited-quirks**, and **quirks**. The chosen doctype - or its absence - is what selects the mode. The modern doctype is deliberately short:

```html
<!DOCTYPE html>
```

**Listing 1.** The only doctype a new document needs; case does not matter.

Older documents carried long doctypes with public identifiers and a DTD URL, because they pointed a validating SGML parser at a version of the language:

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
```

**Listing 2.** An HTML 4.01 Strict doctype; browsers today recognize it only to pick the rendering mode.

The standard explains that doctypes are required "for legacy reasons": when omitted, browsers use a rendering mode that is incompatible with some specifications. Including one ensures a best-effort standards-compliant render. See [[What is HTML]] for where the preamble sits in the document skeleton and [[What is the HTML head element for]] for what follows it.

## What changes in quirks mode

Quirks mode is not cosmetic. It changes measurable layout behavior, the classic examples being the interpretation of the CSS box model and vertical alignment of images in table cells, plus case-insensitive class and id matching in selectors. Because the differences live in the layout engine, a page can look subtly broken only in quirks mode - which makes a forgotten doctype a real-world bug class.

```d2
direction: right
input: "Parser reads the preamble" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
doctype: "<!DOCTYPE html> present?" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
standards: "no-quirks mode\nspecs followed" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
quirks: "quirks mode\nlegacy layout" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
input -> doctype
doctype -> standards: yes
doctype -> quirks: absent
```

**Fig. 1.** The doctype is the switch that picks the rendering mode before any element is parsed.

> [!warning] A comment before the doctype can trigger quirks in old engines
> In Internet Explorer 9 and older, anything before the doctype - even an HTML comment - threw the document into quirks mode. Modern engines ignore such comments, so the safe convention is: doctype first, nothing above it.

> [!tip] Interview answer
> **DOCTYPE is the mandatory preamble that tells the browser to render in standards mode. It is not a tag but a parser instruction; the modern form is just <!DOCTYPE html>. Without it the page falls back to quirks mode, which emulates pre-standards layout engines and changes the box model and other layout behavior.**
