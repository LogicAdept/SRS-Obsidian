<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# How do you write a custom HealthIndicator in Spring Boot?

> [!abstract] Short answer
> Register a Spring bean that implements **`HealthIndicator`** and return a **`Health`** from **`health()`** (`Health.up()`, `Health.down().withDetail(…)`, and so on). The JSON key is the bean name **without** a trailing **`HealthIndicator`** (`MyHealthIndicator` → **`my`**). Component names and details are hidden unless **`management.endpoint.health.show-details`** / **`show-components`** is not the default **`never`**.

## Implement `health()`, return `Health`

Actuator collects every **`HealthContributor`** in the `HealthContributorRegistry`. A **`HealthIndicator`** is the leaf that supplies a **`Status`**. Boot 4’s types live in **`org.springframework.boot.health.contributor`**.

```java
@Component
public class MyHealthIndicator implements HealthIndicator {

	@Override
	public Health health() {
		int errorCode = check();
		if (errorCode != 0) {
			return Health.down().withDetail("Error Code", errorCode).build();
		}
		return Health.up().build();
	}

	private int check() {
		return 0;
	}
}
```

**Listing 1.** Official pattern: status plus optional details. `check()` is your dependency probe. WebFlux: implement **`ReactiveHealthIndicator`** and return **`Mono<Health>`** (or extend `AbstractReactiveHealthIndicator`).

The overall `/actuator/health` status is a **`StatusAggregator`** over all indicators (first of the ordered list wins; unknown statuses become **`UNKNOWN`**). A **`DOWN`** custom indicator makes the aggregate **DOWN** (HTTP **503** by default) ([[How does the Actuator health endpoint aggregate status]]). Disable a built-in with `management.health.<key>.enabled`.

```properties
management.endpoint.health.show-details=always
management.endpoint.health.show-components=always
```

**Listing 2.** Values are `never` (default), `when-authorized`, `always`. `when-authorized` uses `management.endpoint.health.roles` (no roles ⇒ any authenticated user).

```d2
direction: right
bean: "MyHealthIndicator\nHealth.down()/up()" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
reg: "HealthContributorRegistry\nkey: my" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
json: "/actuator/health\nshow-details" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

bean -> reg -> json
```

**Fig. 1.** Bean naming strips the `HealthIndicator` suffix. Details still depend on **show-details** / **show-components** ([[Which Actuator endpoints are exposed over HTTP by default]]).

Custom `Status` codes (for example `FATAL`) need `management.endpoint.health.status.order` and usually `http-mapping` (custom HTTP mappings **replace** the default 503 map unless you restate `down` and `out-of-service`). Indicators that take **> 10s** log a slow warning (`management.endpoint.health.logging.slow-indicator-threshold`).

> [!warning] Details default to hidden
> A working indicator can still look like a bare `{ "status": "UP" }`. **`show-details`** and **`show-components`** default to **`never`**. `always` on a secured app also requires the security chain to **permit** `/actuator/health` for anonymous users if you want probes to see details. The endpoint itself must be **exposed** ([[How do you expose Spring Boot Actuator endpoints safely]]).

> [!warning] Name, speed, and reactive type
> Rename the bean and the health key changes (`myHealthIndicator` is not `my`). Do not block a **WebFlux** event loop with a servlet `HealthIndicator` that talks to a remote API — use **`ReactiveHealthIndicator`**. A custom status absent from **`status.order`** is treated as **`UNKNOWN`**, which still maps to HTTP **200**.

> [!tip] Interview answer
> I implement HealthIndicator as a @Component, return Health.up or Health.down with details from health(), and Boot publishes it under the bean name minus the HealthIndicator suffix. The aggregate status can go DOWN because of that one indicator. Details stay off until I set show-details; reactive apps should use ReactiveHealthIndicator instead.
