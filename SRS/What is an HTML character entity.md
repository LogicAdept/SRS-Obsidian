<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What is an HTML character entity?

> [!abstract] Short answer
> **A character entity (character reference) is an `&`-prefixed escape that stands for another character** - used to write characters that are reserved in HTML syntax, invisible, or hard to type. There are three forms: named references like `&lt;`, decimal numeric `&#60;`, and hexadecimal `&#x3C;`.

## The three forms

```html
<p>1 &lt; 2 &amp;&amp; 3 &gt; 2</p>   <!-- named -->
<p>&#60;same&#62;</p>                  <!-- decimal: code point 60 is '<' -->
<p>&#x3C;same&#x3E;</p>                <!-- hexadecimal -->
```

**Listing 1.** All three forms produce the same visible characters.

The WHATWG syntax requires every character reference to start with `&`. A **named** reference uses one of the names from the standard's named-references list and must be terminated by a semicolon in valid markup. Numeric references take the code point directly: `&#60;` for `<`, `&#x3C;` for the same point in hex.

> [!warning] Missing semicolon changes the meaning
> In HTML5 parsing an ampersand not forming a valid reference is often rendered literally, but legacy parsing rules made things like `&notin;` ambiguous: some browsers historically rendered it as the entity not followed by "in". Always terminate named references with `;` - and remember that the reserved characters in text content are `<`, `&`, and (in attribute values with the same quote) the quote itself.

## Why entities exist

Two honest purposes:

1. **Escaping reserved syntax characters.** To show `<`, `>`, or `&` as text, they must be escaped or the parser would read them as markup.
2. **Writing untypeable characters.** Symbols, typographic dashes, or non-keyboard characters can be inserted by name or code point regardless of file encoding - although with UTF-8 as the default encoding, most modern documents only need the reserved-character escapes. See [[What is HTML]] for how the parser treats text and [[What is the HTML head element for]] for the charset declaration that reduces the need for escapes.

```d2
direction: right
amp: "& starts a reference" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}
named: "named: &lt; &amp; &copy;" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
dec: "decimal: &#60;" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
hex: "hex: &#x3C;" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
amp -> named
amp -> dec
amp -> hex
```

**Fig. 1.** One entry point, three forms - all resolving to a single character.

> [!tip] Interview answer
> **A character entity is the HTML escape for a single character: named (&lt;, &amp;), decimal (&#60;), or hex (&#x3C;). It exists to escape syntax-reserved characters and to type characters the keyboard or encoding cannot. Named references must end with a semicolon.**
