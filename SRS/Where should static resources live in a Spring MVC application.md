<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot/AutoConfiguration #SRS

# Where should static resources live in a Spring MVC application?

> [!abstract] Short answer
> **In Spring Boot**, put CSS/JS/images (and `index.html` / `favicon.ico`) on the classpath under **`/static`**, **`/public`**, **`/resources`**, or **`/META-INF/resources`** (typical: `src/main/resources/static/`). They are served from **`/**`** via **`ResourceHttpRequestHandler`**. **Classic MVC** has no those four folders unless you call **`WebMvcConfigurer.addResourceHandlers`**. You can always remap with **`spring.mvc.static-path-pattern`** / **`spring.web.resources.static-locations`**.

## Boot defaults vs explicit handlers

Boot also serves from the **ServletContext root** and maps **`/webjars/**`** to WebJar classpath entries. Welcome page: first `index.html` in those locations, else an `index` template. `@EnableWebMvc` **turns off** `WebMvcAutoConfiguration`, including this static setup — then you must register handlers yourself.

Framework MVC example: map URL prefix `/resources/**` to `/public` (web root) and `classpath:/static/`, with long `Cache-Control`. Optional `VersionResourceResolver` for content hashes. `EncodedResourceResolver` (gzip/brotli) must run **before** versioning so hashes are of the raw file.

```text
src/main/resources/static/css/app.css
src/main/resources/static/js/app.js
src/main/resources/public/index.html
```

**Listing 1.** Conceptual Boot layout. URL `/css/app.css` unless you change `spring.mvc.static-path-pattern`. Config SPI: [[What is WebMvcConfigurer in Spring MVC]]. `@EnableWebMvc` risk: [[What is the EnableWebMvc annotation]]. View names vs files: [[What is a ViewResolver in Spring MVC]].

```java
@Override
public void addResourceHandlers(ResourceHandlerRegistry registry) {
    registry.addResourceHandler("/resources/**")
            .addResourceLocations("/public", "classpath:/static/")
            .setCacheControl(CacheControl.maxAge(Duration.ofDays(365)));
}
```

**Listing 2.** Conceptual Framework: explicit locations and cache. Boot equivalent: `spring.web.resources.static-locations`.

```d2
direction: down
cp: "classpath:/static\n/public /resources\n/META-INF/resources" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
h: "ResourceHttpRequestHandler\n/**" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
b: "browser /css/app.css" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

cp -> h
h -> b
```

**Fig. 1.** Boot maps `/**` to those directories. Controllers still win for overlapping `@RequestMapping` paths; leftover URLs that miss a file become **`NoResourceFoundException`**, not `NoHandlerFoundException`, until you narrow `static-path-pattern` or set `spring.web.resources.add-mappings=false`.

> [!warning] `/**` swallows 404 mapping
> Default static mapping handles **every** unmatched path. For a true `NoHandlerFoundException`, restrict the static pattern or disable resource mappings.

> [!warning] `@EnableWebMvc` in Boot
> Importing full MVC config **drops** Boot’s static resource auto-config. Either skip `@EnableWebMvc` or re-declare `addResourceHandlers`.

> [!warning] Not `WEB-INF` for public assets
> Files under `WEB-INF` are **not** served by URL. Use classpath `static/` (Boot) or an explicit `addResourceLocations` that is web-reachable.

> [!tip] Interview answer
> **Boot: `src/main/resources/static` (or `public` / `resources` / `META-INF/resources`).** Served from `/**`. Classic Spring MVC: call `addResourceHandlers` — those four folders are a Boot convention, not a Framework default.
