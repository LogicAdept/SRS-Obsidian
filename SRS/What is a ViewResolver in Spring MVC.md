<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A controller returns a **logical view name**. `ViewResolver` turns that name into a `View` (JSP, FreeMarker, …).

Dumps name `UrlBasedViewResolver` (direct name → URL), `ContentNegotiatingViewResolver` (pick a view from the client’s media type: XML, JSON, PDF), and technology-specific resolvers (`FreeMarkerViewResolver`). Velocity/Jasper resolvers appear in older lists.

POJO controllers stay reusable because they do not hard-code the rendering technology.

> [!warning] Unverified traps from the dump
> - `@RestController` / `@ResponseBody` skip view resolution and write the body via message converters.
> - Several resolvers can be chained; order matters.
