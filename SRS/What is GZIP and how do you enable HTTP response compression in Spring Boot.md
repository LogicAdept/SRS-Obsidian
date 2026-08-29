<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Networking/Web #SRS

# What is GZIP and how do you enable HTTP response compression in Spring Boot?

> [!abstract] Short answer
> **GZIP** (RFC **1952**) is a **lossless** wrapper around **DEFLATE** (RFC **1951**), with a CRC. In HTTP, **`Content-Encoding: gzip`** compresses the representation without changing **`Content-Type`** (client advertises **`Accept-Encoding`**). Boot: **`server.compression.enabled=true`** (default **`false`**). Applies to **embedded** Jetty, Tomcat, and Reactor Netty. Default floor is **2KB** (`min-response-size`); default MIME list is HTML/XML/plain/CSS/JS/JSON.

## Encoding vs Boot’s server property

HTTP uses gzip as a **content coding**. Boot does **not** invent gzip; the embedded server compresses matching responses when the client accepts it.

```properties
server.compression.enabled=true
```

**Listing 1.** Official enable. Appendix default is **`false`**. Threshold: **`server.compression.min-response-size`** — default **`2KB`** (2048 bytes), not 1KB. That value is a **`Content-Length`** floor.

Default MIME types (replace with **`server.compression.mime-types`**, or **add** with **`server.compression.additional-mime-types`**):

- `text/html`, `text/xml`, `text/plain`, `text/css`, `text/javascript`
- `application/javascript`, `application/json`, `application/xml`

```properties
server.compression.min-response-size=2KB
server.compression.excluded-user-agents=
```

**Listing 2.** `min-response-size` accepts Boot **`DataSize`** (`1024`, `1KB`, `2KB`). **`excluded-user-agents`** skips named clients. This is **not** `spring.web.resources.chain.compressed` (serve pre-built `.gz` / `.br` static files).

```d2
direction: down
req: "Accept-Encoding: gzip" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
boot: "server.compression.enabled\nmime + min size" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
res: "Content-Encoding: gzip\n(same Content-Type)" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}

req -> boot -> res
```

**Fig. 1.** Already-compressed payloads (JPEG, ZIP) should **not** be in `mime-types`. SSL is a separate `server.ssl.*` story ([[How do you enable HTTPS in a Spring Boot application]]). An **external** Tomcat you deploy a WAR into is **not** configured by these Boot properties ([[How do you deploy a Spring Boot application as a WAR]], [[Which embedded containers are supported by Spring Boot]]).

> [!warning] Dump numbers are not the defaults
> Enabling with a hand-picked MIME list that **omits** `application/json` / `application/javascript` **replaces** the defaults if you set `mime-types`. Default minimum is **2048 bytes**, not 1024. There is **no** official “saves 50%” figure. Current how-to lists **Jetty, Tomcat, Reactor Netty** — not a guarantee for every reverse proxy.

> [!warning] Tiny JSON will not gzip
> Under **2KB**, Boot leaves the body uncompressed even when enabled. Gzip is **lossless**; it is **not** encryption. Double compression (app gzip + CDN gzip) wastes CPU.

> [!tip] Interview answer
> GZIP is DEFLATE plus a header and CRC. HTTP uses Content-Encoding gzip when the client sends Accept-Encoding. In Spring Boot I set server.compression.enabled to true on the embedded server. Defaults are 2KB minimum and a standard text/JSON MIME list; I add types with additional-mime-types so I do not wipe the defaults.
