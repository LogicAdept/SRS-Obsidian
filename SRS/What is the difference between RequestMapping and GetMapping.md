<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@RequestMapping` maps any HTTP method (set `method = RequestMethod.GET`, or omit for all methods in older usage).

`@GetMapping` is a composed annotation: `@RequestMapping` with GET only. Same family: `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`.

```java
@RequestMapping(value = "/home", method = RequestMethod.GET)
@GetMapping("/home")
```

> [!warning] Unverified traps from the dump
> - Class-level @RequestMapping still combines with method-level @GetMapping.
> - A nearby card compares @RequestMapping with @PutMapping; this one is the GET shortcut.
