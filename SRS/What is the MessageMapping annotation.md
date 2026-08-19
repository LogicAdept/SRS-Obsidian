<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@MessageMapping` routes incoming STOMP destinations to a controller method, analogous to `@RequestMapping` for HTTP. Client SEND `/app/hello` maps to `@MessageMapping("/hello")` when `/app` is the application prefix.

Payload is deserialized (Jackson in dumps). Combine with `@SendTo` or send via `SimpMessagingTemplate`.

> [!warning] Unverified traps from the dump
> - It is not an HTTP mapping. `@GetMapping` will not receive STOMP SEND frames.

