<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use `@RequestMapping(method = …)` or the composed annotations:

- GET → `@GetMapping`
- POST → `@PostMapping`
- PUT → `@PutMapping`
- DELETE → `@DeleteMapping`
- PATCH → `@PatchMapping`

Dumps: GET retrieve, POST create, PUT update, DELETE delete, PATCH partial update.

> [!warning] Unverified traps from the dump
> - Class-level @RequestMapping prefixes all method mappings.
