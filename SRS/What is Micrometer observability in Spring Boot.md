<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# What is Micrometer observability in Spring Boot?

> [!abstract] Short answer
> Official definition: **observability** is seeing a running system **from the outside**. Three **pillars**: **logging**, **metrics**, **traces**. For **metrics and traces**, Boot uses **Micrometer Observation**: inject **`ObservationRegistry`**, start an **`Observation`**; handlers turn it into a **timer** and (with Micrometer Tracing) a **span**. Logs stay logs; Boot can put **`traceId`/`spanId`** in the MDC. This is **not** Spring Boot Admin and **not** a log replacement.

## One observation, two backends

Boot auto-configures **`ObservationRegistry`**. Completing an observation: **`DefaultMeterObservationHandler`** → Micrometer **metrics**; **`TracingAwareMeterObservationHandler`** → **spans** if a tracer is on the classpath (Brave/Zipkin or OpenTelemetry/OTLP) ([[What changed in Spring Boot 3]], [[How do you monitor an application with Spring Boot Actuator]]).

```java
@Component
public class MyCustomObservation {

	private final ObservationRegistry observationRegistry;

	public MyCustomObservation(ObservationRegistry observationRegistry) {
		this.observationRegistry = observationRegistry;
	}

	public void doSomething() {
		Observation.createNotStarted("doSomething", this.observationRegistry)
			.lowCardinalityKeyValue("locale", "en-US")
			.highCardinalityKeyValue("userId", "42")
			.observe(() -> {
				// business logic
			});
	}
}
```

**Listing 1.** Official custom observation. **Low-cardinality** keys go on **metrics and traces**; **high-cardinality** keys go on **traces only** (keep them off meters). Span **without** a metric: Micrometer **`Tracer`**, not `Observation`.

Beans auto-registered on the registry: **`ObservationPredicate`**, **`GlobalObservationConvention`**, **`ObservationFilter`**, **`ObservationHandler`**, plus **`ObservationRegistryCustomizer`**. Common tags: `management.observations.key-values.*`. Disable a name prefix: `management.observations.enable.<name>=false`.

Tracing: default **sample 10%** (`management.tracing.sampling.probability`). Starters: **`spring-boot-starter-zipkin`** (Brave) or **`spring-boot-starter-opentelemetry`**. Propagate with auto-configured **`RestClient.Builder` / `RestTemplateBuilder` / `WebClient.Builder`**. Logs: default correlation **`[traceId-spanId]`**. Prometheus scrape is **`micrometer-registry-prometheus`** + Actuator **`prometheus`** endpoint — **not** the same as Zipkin.

```d2
direction: down
obs: "ObservationRegistry\nObservation.observe" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
met: "metrics\n(MeterRegistry / Prometheus)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
tr: "traces\n(Brave / OTel → Zipkin / OTLP)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
log: "logs + MDC traceId/spanId" {
  width: 280
  height: 50
  style.fill: "#f3e5f5"
}

obs -> met
obs -> tr
obs -> log
```

**Fig. 1.** Annotations (`@Observed`, `@Timed`, …) need **`management.observations.annotations.enabled=true`** and **AspectJ**. Do not stack them on already-instrumented MVC/Data methods (duplicate observations). Prefer Observation/Tracing APIs over raw OpenTelemetry in a Boot app. Metrics still go through **Micrometer**, not OTel’s `SdkMeterProvider`.

> [!warning] Observation is not “logs vs metrics vs traces as three products”
> One API feeds **metrics and traces**. **Logging** is still Logback/Log4j; correlation IDs **link** lines to spans. `@Async` needs **`spring.task.execution.propagate-context`** (or a `ContextPropagatingTaskDecorator`). Reactor: **`spring.reactor.context-propagation=auto`**. `httpexchanges` is a **dev** in-memory recorder, not production tracing.

> [!warning] `@SpringBootTest` does not auto-configure reporting tracers
> Tests skip the exporters. Sampling at **10%** means most local requests never hit Zipkin unless you raise probability. Building `RestClient` **without** Boot’s builder **drops** propagation.

> [!tip] Interview answer
> Observability is logs, metrics, and traces. Boot 3+ uses Micrometer Observation so one ObservationRegistry call can time a metric and open a span. I keep user ids on traces only. Logs get traceId in the MDC. Prometheus scrapes meters; Zipkin or OTLP gets traces. It does not replace logging.
