<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`MultipartResolver` handles **file upload** requests. It is not on by default in classic Spring MVC: you register an implementation in configuration. After that, upload requests are parsed through this resolver so a controller can receive `MultipartFile`.

Boot enables multipart via `spring.servlet.multipart.*` (max file size, threshold, and so on) instead of a manual XML `MultipartResolver` bean.

> [!warning] Unverified traps from the dump
> - Without a resolver (or Boot multipart auto-config), `MultipartFile` parameters will not bind.
> - This is the MVC-side parser; storage location is a separate concern.
