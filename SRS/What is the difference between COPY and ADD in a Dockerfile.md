<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the difference between COPY and ADD in a Dockerfile

> [!abstract] Short answer
> `COPY` does one thing: copies files from the build context into the image. `ADD` does `COPY` plus magic — it auto-extracts local tar archives and can fetch a remote URL or a Git repository. Docker's own guidance is to prefer `COPY` unless you specifically need the extraction or download behavior.

## What ADD adds

`ADD` supports three source kinds: build-context paths, a remote URL (downloaded but **not** unpacked), and a Git repository (cloned). For a **local tar archive** it decompresses and extracts at the destination; a tar fetched by URL lands as a plain file.

```dockerfile
COPY target/app.jar /app/app.jar          # plain copy — the default choice
ADD bundle.tar.gz /opt/service/           # ADD = COPY + auto-extract for local tars
ADD vendored.tar.gz /tmp/                 # a URL source would download but NOT extract
```

**Listing 1.** The ADD behaviors side by side; only a local tar gets unpacked, and a URL source (address omitted deliberately) would land as a plain file in a layer. Configuration snippets like this are not executed during review — they illustrate the reference contract.

That one-line extraction is the legitimate use case; everything else is clearer as `COPY`, which is why review feedback usually rewrites `ADD` into `COPY` — matching how multi-stage builds split toolchain from artifact ([[How would you explain Multi-stage build]]).

> [!warning] ADD <URL> bloats and busts the cache
> A remote URL source downloads the file into a layer at build time: it stays in the image forever (the layer cannot be shrunk by a later delete — [[How do Docker image layers relate to a Dockerfile]]), and the layer is invalidated on every content change. For remote resources the idiomatic move is `RUN curl -fsSL url | tar -xz -C /opt` in one layer, or fetching in a builder stage and `COPY --from` only the result.

> [!tip] Interview answer
> **COPY copies from the build context, period. ADD is COPY plus auto-extraction of local tar archives plus URL/Git sources. Prefer COPY for predictability; use ADD for its tar unpacking; avoid ADD with URLs because the download bakes into a layer and busts the cache.**

