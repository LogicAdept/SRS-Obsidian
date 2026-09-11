<!--
reps: 0
priority: 0
-->
#Testing/Performance #SystemDesign/Performance #SRS

# What is load testing

> [!abstract] Short answer
> Load testing drives a system with realistic, expected-level traffic to measure how it behaves at operating load — throughput, latency percentiles, error rate, resource usage — and to find where it saturates. It answers "can we serve the expected traffic with acceptable latency?", distinguishing itself from stress testing (beyond capacity, to find breaking points), spike testing (sudden surges) and soak testing (long duration, to catch leaks and degradation).

## The shapes of load

The k6 testing taxonomy names the families: smoke tests (a minimal load to verify the harness works), load tests (the expected peak — constant or ramped to it), stress tests (load past the expected maximum until the system breaks, to find the ceiling and observe the failure mode), spike tests (near-instant jumps above peak — deploy-day traffic or a marketing event), and soak tests (moderate load for hours or days, surfacing memory leaks, connection-pool exhaustion, log growth, cache degradation). A load test is defined by a workload model (how many virtual users, what request mix, what think time — matching production traffic shape, not a uniform hammer) and pass/fail criteria — the SLOs: p95 under 300 ms, error rate below 0.1%. Without SLO-based thresholds, the result is a graph, not a verdict; [[How do you monitor database health and load]] frames where those numbers come from.

```text
load   : ramp to expected peak, hold 30m      -> p95, error%, saturation point
stress : increase past peak until failure     -> ceiling + failure mode
spike  : peak -> 3x in 10s -> back            -> recovery time
soak   : 50% load for 24h                     -> leaks, slow degradation
```

**Listing 1.** The four shapes and what each one answers.

## Reading the results and the common traps

The deliverables are the numbers at target load (throughput at the SLO's latency — not raw max throughput), the saturation point and its bottleneck (CPU, connection pool, lock, downstream limit), and the failure mode under stress (graceful degradation versus collapse). Classic traps invalidate the test before it runs: measuring from the load generator only (the network and client TLS matter), a generator too weak to produce the load (so the system "passes" at half the intended rate), a uniform workload unlike production's skew (hot keys dominate real traffic — [[What is cold data and hot data]]), and cold caches making the first minutes unrepresentative ([[What difficulties arise when working with caching]]). Results feed the scaling decisions: whether to add replicas, tune pools, or shard ([[What problem does database sharding solve]]), and they pair with resilience checks — the system under load is also the one that must survive a two-second blip ([[How do you handle a two second network outage]]), which is why stress and chaos often share a test rig.

> [!warning] Load testing a system that caches itself green
> Running the same scripted scenario daily warms every cache and learns nothing new — the system passes at 10x while a fresh-deploy cold start would collapse. Reset state or model cold-start scenarios deliberately, or the test measures yesterday's warmth.

> [!tip] Interview answer
> Load testing applies realistic expected traffic against explicit SLOs to measure throughput, latency percentiles and the saturation point. I distinguish stress (find the ceiling and failure mode), spike (sudden surges) and soak (long-run leaks), and I validate the rig itself: realistic workload mix, a generator strong enough, cold-cache awareness — otherwise the numbers are theater.
