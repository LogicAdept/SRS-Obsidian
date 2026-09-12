<!--
reps: 0
priority: 0
-->
#Networking/Web/MIME #SRS
# What is a MIME type

> [!abstract] Short answer
> A MIME type (media type) is the label `type/subtype` — like text/html or application/json — that tells a receiver how to interpret a body. Defined originally for email (RFC 2046), it is now how HTTP self-describes payloads: the server declares Content-Type, the client declares what it accepts (Accept), and browsers, proxies and caches make decisions — render, download, cache — based on that label. The authoritative registry is IANA's media-types list.

## Structure and the working set

`type/subtype` plus optional parameters: `text/html; charset=utf-8`, `application/json`, `image/png`, `multipart/form-data; boundary=...`.

- **text/** — human-readable: text/html, text/css, text/plain, text/csv.
- **application/** — machine formats: application/json, application/xml, application/pdf, application/octet-stream (the "opaque bytes" default), application/x-www-form-urlencoded (classic form POST), application/vnd.api+json (vendor + suffix style).
- **image/, audio/, video/** — media (image/svg+xml shows the structured subtypes).
- **multipart/** — composite bodies: multipart/form-data (file uploads), multipart/byteranges (range responses).

```d2
direction: right
srv: "Server sends\nContent-Type: application/json" { width: 270; height: 90; style.fill: "#fff3e0" }
br: "Browser / client\nchecks Accept, then type" { width: 250; height: 90; style.fill: "#e3f2fd" }
dec: "Decision:\nrender | download | parse | reject" { width: 280; height: 90; style.fill: "#e8f5e9" }
srv -> br -> dec
```

**Fig. 1.** The label is the contract that turns bytes into behavior — mislabeled bytes get the wrong behavior.

## Where it bites in practice

- **Content negotiation:** the client sends `Accept: application/json`; the server picks the representation and returns its Content-Type — the REST response contract ([[Which HTTP status codes matter most in REST API design]]: 406/415 live here).
- **Sniffing vs labeling:** browsers historically guessed types of unlabeled responses (MIME sniffing); `X-Content-Type-Options: nosniff` forbids it — because serving user-uploaded HTML as text/plain is the difference between safe display and stored XSS.
- **Downloads:** `Content-Disposition: attachment` (not a MIME type itself) forces download instead of render.
- **Java/Spring:** mapping extensions to types via content negotiation and `MediaType` constants; wrong type → browser renders JSON as text or refuses a stylesheet (strict MIME checking on scripts/styles).

> [!warning] "The file extension defines the type" — servers do, and wrongly set types are a bug
> The Content-Type header is authoritative on the web; extensions matter only as the server's hint when *choosing* the header. Classic failures: serving JSON as text/plain (some tools stop parsing), serving user uploads as text/html (XSS via nosniff-absent browsers), and forgetting charset — the bytes are UTF-8 but the header says nothing, so the browser guesses. Also: MIME types describe *representations*, not resources — one URI can serve image/png or application/json depending on negotiation ([[What are the parts of an HTTP request]] shows where both headers ride).

Transport context: [[What is HTTP]], [[What is GZIP and how do you enable HTTP response compression in Spring Boot]] (Content-Encoding is orthogonal to Content-Type).

> [!tip] Interview answer
> A MIME type is the type/subtype label — text/html, application/json, image/png — that tells the receiver how to interpret the body, with parameters like charset. It powers content negotiation via Accept/Content-Type, file uploads as multipart/form-data, and security-sensitive decisions like nosniff. The pitfalls I name: the header is authoritative over extensions, missing charsets cause mojibake, and labeling uploads as HTML is an XSS vector.
