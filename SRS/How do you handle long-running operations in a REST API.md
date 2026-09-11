<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# How do you handle long-running operations in a REST API

> [!abstract] Short answer
> Do not hold the HTTP connection. Return 202 Accepted immediately with a Location header pointing at a status resource; the client polls that resource (or subscribes to a callback/stream) until it reports completion and the result URI. Make the operation's creation idempotent, the status resource cache-friendly, and the polling interval adaptive.

## The 202-plus-status-resource pattern

The synchronous request/response contract assumes the answer arrives in the connection's lifetime; exports, bulk imports, and report generation violate that. The pattern: POST /exports validates the request and enqueues the work, then answers 202 Accepted with Location: /exports/jobs/1 — the job resource. GET on the job returns state (queued, running, done), progress if meaningful, and, when done, the result URI in the body and Location. Some designs answer the final poll with 303 See Other to the result; the body-with-result-URI variant is simpler and cache-friendlier. The job resource is itself a resource: addressable, cacheable while running (short max-age or ETag so polling is cheap), and gone or 410 after its retention window. Polling can be tuned with Retry-After on in-progress responses; webhooks or SSE replace polling entirely when the client is a server ([[What are webhooks and how do you implement them reliably]] for the push side; [[Which HTTP status codes matter most in REST API design]] for where 202 sits).

```text
server: POST /exports -> 202 Accepted, Location=/exports/jobs/1
client POST: 202 (202 -> poll, not the result)
client GET /exports/jobs/1: 200 {"jobId":1,"status":"running","progress":60}
client GET /exports/jobs/1: 200 {"jobId":1,"status":"done","progress":100,"result":"/exports/files/9"}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): 202 with Location, then a status resource progressing queued -> running -> done with the result URI (out/A07_LongRunning.txt).

```d2
c: client
api: API
w: worker (async)
c -> api: POST /exports
api -> c: 202 + Location /jobs/1
api -> w: enqueue
c -> api: GET /jobs/1
api -> c: 200 running 60%
w -> api: job completes
c -> api: GET /jobs/1
api -> c: 200 done + result /files/9
c -> api: GET /files/9
```

**Fig. 1.** The request completes at 202; the job resource tracks progress and finally hands over the result URI.

## The engineering details that decide success

Idempotent creation: a client retrying the POST (timeout after enqueue) must not enqueue twice — accept an Idempotency-Key or derive job identity from the request ([[What is the Idempotency-Key header used for in HTTP APIs]], [[What is idempotency in HTTP and in messaging]]). Progress and cancellation: a DELETE on the job resource gives clients a cancellation story; progress percentages require real instrumentation, so ship them only when cheap. Timeout arithmetic: pick client poll intervals with backoff, set job retention, and decide what an abandoned job's result does. The contrast interviewers draw: blocking long requests exhausts thread pools and proxy timeouts (and invites silent duplicated work on retry), while fire-and-forget without a status resource leaves clients blind. Async-first frameworks (WebFlux, virtual threads on JDK 21) stretch the synchronous limit but do not change the contract at minutes-plus scales ([[How does the WebFlux event loop work]] for why blocking is costlier than it looks).

> [!warning] A retried 202 request is a second job
> If POST /exports enqueues then the response is lost, the client's retry enqueues again — two exports, doubled cost. Long-running endpoints need the same idempotency-key discipline as payment endpoints, plus job deduplication on request identity.

> [!tip] Interview answer
> I return 202 Accepted with a Location header to a job resource and let clients poll it or subscribe — never hold the connection. The job exposes status, progress, cancellation via DELETE, and finally the result URI; responses carry short freshness so polling is cacheable. Creation is idempotent via an idempotency key, since a lost 202 response will be retried, and I set retention and Retry-After explicitly.
