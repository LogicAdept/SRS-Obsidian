<!--
reps: 0
priority: 0
-->
#Networking/Web/UrlEncoding #Java/Networking/UrlEncoding #SRS

# What is URL encoding and how do you perform it in Java

> [!abstract] Short answer
> **URL (percent) encoding replaces characters that are unsafe or reserved in a URL with `%XX` byte sequences.** In Java: `URLEncoder.encode(String, Charset)` — but note its javadoc frame: it converts to the `application/x-www-form-urlencoded` format (spaces become `+`), the HTML *form* convention. For strict RFC percent-encoding in a URL path (spaces as `%20`), use `URI`/`UriComponentsBuilder`-style building instead.

## The rules (from the javadoc)

For `URLEncoder.encode`: alphanumerics stay; the special characters `.`, `-`, `*`, `_` stay; the space becomes `+`; everything else is converted to bytes (UTF-8 in the Charset overload) and each byte is written as a `%XX` escape. `URLDecoder.decode` reverses it exactly.

```java
String raw = "a b&c=1";
String enc = URLEncoder.encode(raw, StandardCharsets.UTF_8);
System.out.println("encoded: " + enc);
System.out.println("decoded: " + URLDecoder.decode(enc, StandardCharsets.UTF_8));
```

**Listing 1.** Verified on JDK 21:

```java
encoded: a+b%26c%3D1
decoded: a b&c=1
```

**Listing 2.** Watch the symbols: the space became `+`, `&` became `%26`, `=` became `%3D` — reserved query characters must be escaped or they change meaning; round-tripping restores the original exactly.

```d2
direction: right
raw: "Raw value\n\"a b&c=1\"" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
enc: "URLEncoder.encode\n\"a+b%26c%3D1\"" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
url: "Safe inside a URL\nquery parameter" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
dec: "URLDecoder.decode\nround-trips back" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
raw -> enc -> url
enc -> dec
```

**Fig. 1.** Encode at the boundary where a value becomes part of a URL; decode where it comes back out.

## Encode at the right place

The rule that keeps APIs correct: values are encoded when *assembled into* a URL — never encode a whole URL string (that escapes the `://` and `?` you need), and never double-encode (a stored `%2F` decoded twice turns into `/`). Reserved delimiters — `&`, `=`, `?`, `/`, `#` — are exactly why: an unencoded `&` inside a query value splits the parameter into two, an unencoded `#` terminates the query into a fragment.

> [!warning] URLEncoder is form encoding, not RFC 3986 path encoding
> The classic Java trap, in three flavors. First, the space: `URLEncoder` produces `+` (form convention); a strict URL parser expecting `%20` may treat `+` as a literal plus — API paths built with URLEncoder have broken spaces in exactly the systems that follow the RFC. Second, it is a *component* encoder — running it on a full URL escapes the structural characters and produces garbage. Third, legacy: the one-argument `URLEncoder.encode(String)` uses the platform default charset — a bug factory replaced by the Charset overload since Java 10 (deprecated since Java 9). Decoding has the mirror trap: `URLDecoder` turns both `+` and `%20` into a space, so a genuinely intended `+` must be sent as `%2B`. The target-type distinction (form data versus URL components) is the answer interviewers actually want — see [[How would you explain TCP or UDP sockets in Java networking]] for the transport underneath and [[What is the difference between HTTP 401 and 403]] for one classic consequence of misencoded auth URLs.

> [!tip] Interview answer
> **URL encoding replaces unsafe or reserved characters with %XX byte escapes so values survive inside URLs. In Java, URLEncoder.encode with an explicit Charset — spaces become +, & becomes %26, = becomes %3D; URLDecoder reverses it. Key nuance: URLEncoder implements the application/x-www-form-urlencoded form convention, not RFC path encoding — for URL paths build URIs instead, and never encode an entire URL.**

