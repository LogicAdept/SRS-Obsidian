<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

WebFlux uses the Reactive Streams standard for async streams with non-blocking backpressure, implemented via Project Reactor. Example they paste: `Flux.range(...).onBackpressureBuffer(10).subscribe(...)`.

clients `request(n)`; `limitRate()` throttles so the client is not flooded.

if a source emits 10,000/sec and the DB saves 100/sec, buffer/drop/latest strategies stop OOM.

> [!warning] Unverified traps from the dump
> - General backpressure already has `#Paradigms/Reactive` cards; this cue is the WebFlux-interview wording.
> - One dump names HTTP/TCP flow control as natural backpressure over the wire.

