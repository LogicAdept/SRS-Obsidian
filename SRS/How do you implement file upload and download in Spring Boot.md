<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebMvc #SRS

# How do you implement file upload and download in Spring Boot?

> [!abstract] Short answer
> **Upload:** accept `multipart/form-data` with **`@RequestParam MultipartFile`** (or `List<MultipartFile>` / `@RequestPart`). Boot already registers **`StandardServletMultipartResolver`** (`spring.servlet.multipart.enabled=true`). **Copy** the bytes with **`transferTo`** (or a stream) before the request ends — temp storage is **cleared**. **Download:** return **`ResponseEntity<Resource>`** (or `StreamingResponseBody`) and set **`Content-Disposition`** via **`ContentDisposition.attachment()`**. Caps default to **1 MB per file / 10 MB per request**.

## Parse multipart, then persist yourself

MVC *Multipart*: after the resolver wraps the request, parts are ordinary parameters. Named `@RequestParam("file") MultipartFile file`; several files with the same name → `List<MultipartFile>`. Unnamed `Map`/`MultiValueMap` of `MultipartFile` collects **all** parts. JSON + file → **`@RequestPart`** so converters deserialize the metadata part. You can bind `MultipartFile` on a command object. Servlet **`Part`** is also a legal argument.

`MultipartFile` javadoc: contents live **in memory or a temp file**; **you** copy them to durable storage. **`getOriginalFilename()` is client-supplied** — do not use it as a path.

Boot `MultipartProperties`: `max-file-size` **1MB**, `max-request-size` **10MB**, `file-size-threshold` **0**, `location` empty (container temp). Oversize → **`MaxUploadSizeExceededException`** (`MultipartException`).

Download: `ResourceHttpMessageConverter` writes a Spring **`Resource`**. Prefer **`ContentDisposition.attachment().filename(name).build()`** (RFC 6266) over concatenating header strings.

```java
@PostMapping("/files")
public ResponseEntity<Void> upload(@RequestParam("file") MultipartFile file)
        throws IOException {
    Path dest = storageDir.resolve(UUID.randomUUID().toString()); // not the client name
    file.transferTo(dest);
    return ResponseEntity.created(/* uri */).build();
}

@GetMapping("/files/{id}")
public ResponseEntity<Resource> download(@PathVariable String id) {
    Resource body = storage.load(id);
    return ResponseEntity.ok()
            .headers(h -> h.setContentDisposition(
                    ContentDisposition.attachment().filename(body.getFilename()).build()))
            .contentType(MediaType.APPLICATION_OCTET_STREAM)
            .body(body);
}
```

**Listing 1.** Conceptual: persist with `transferTo`; download a `Resource`. Resolver SPI: [[What is a MultipartResolver in Spring MVC]]. Param vs part: [[What is the difference between RequestParam and PathVariable]]. Headers wrapper: [[What is the difference between ResponseBody and ResponseEntity]].

```properties
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

**Listing 2.** Conceptual Boot overrides. Defaults are **1MB / 10MB**, not tutorial “200MB”. `enabled` defaults **true**.

```d2
direction: down
post: "POST multipart/form-data" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
mf: "MultipartFile (temp)" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
disk: "transferTo persistent store" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
get: "GET ResponseEntity<Resource>" {
  width: 280
  height: 45
  style.fill: "#fce4ec"
}

post -> mf
mf -> disk
disk -> get
```

**Fig. 1.** Boot parses the upload; **your** code owns the durable file. Download is a resource write plus `Content-Disposition`.

> [!warning] Client filename is not a path
> `getOriginalFilename()` can contain **`..`** and directory pieces. Generate a stored name. `StringUtils.cleanPath` is not a security boundary by itself.

> [!warning] Temp file dies with the request
> Holding a `MultipartFile` or its stream after the handler returns is undefined. **`transferTo` once**; a second call can fail if the provider **moved** the temp file.

> [!warning] `Resource.getFile()` is not always a `File`
> Classpath or URL resources may throw when you ask for a `java.io.File`. Stream the `Resource` (or `StreamingResponseBody`) instead of `getFile().getAbsolutePath()` for MIME guessing.

> [!tip] Interview answer
> Boot: **`@RequestParam MultipartFile`**, limits via **`spring.servlet.multipart.max-*-size`** (default 1 MB / 10 MB). Copy off the temp store with **`transferTo`**. Download **`ResponseEntity<Resource>`** plus **`ContentDisposition.attachment()`**. Never trust the original filename as a filesystem path.
