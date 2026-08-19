<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@SendTo` sets where the method return value is published. Example: `@MessageMapping("/hello") @SendTo("/topic/greetings")` broadcasts the `Greeting` to every subscriber of that destination.

Using `@SendTo("/topic/...")` for a private reply sends that payload to every connected client. Dumps say use `@SendToUser` for the calling session.

> [!warning] Unverified traps from the dump
> - Default destination without `@SendTo` is dump-specific; do not assume `/topic` plus the input path.

