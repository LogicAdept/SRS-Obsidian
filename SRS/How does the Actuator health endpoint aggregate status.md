<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# How does the Actuator health endpoint aggregate status?

> [!abstract] Short answer
> `/actuator/health` folds every **`HealthContributor`** (`HealthIndicator` or **`CompositeHealthContributor`**) through a **`StatusAggregator`**. The aggregator **sorts** indicator statuses against **`management.endpoint.health.status.order`** and takes the **first** entry. The default order is **`DOWN`, `OUT_OF_SERVICE`, `UP`, `UNKNOWN`**. **`DOWN`** and **`OUT_OF_SERVICE`** map to HTTP **503**; **`UP`** and **`UNKNOWN`** have no mapping, so the response is **200**.

## Ordered list, not a mystery “severity”

Contributors form a **tree**. Leaves return a **`Status`**. Built-in codes are **`UP`**, **`DOWN`**, **`OUT_OF_SERVICE`**, and **`UNKNOWN`**. If **no** indicator returns a status the aggregator knows, the overall status is **`UNKNOWN`**.

Auto-configured examples include **`db`**, **`diskspace`**, **`ping`** (always **`UP`**), **`redis`**, **`ssl`**. Disable one with `management.health.<key>.enabled`; disable the built-in set with `management.health.defaults.enabled`. Custom indicators are extra leaves ([[How do you write a custom HealthIndicator in Spring Boot]]).

```properties
management.endpoint.health.status.order=fatal,down,out-of-service,unknown,up
management.endpoint.health.status.http-mapping.down=503
management.endpoint.health.status.http-mapping.fatal=503
management.endpoint.health.status.http-mapping.out-of-service=503
```

**Listing 1.** Custom `FATAL` in the order list. Any custom **`http-mapping`** **replaces** the default **503** map for `DOWN` / `OUT_OF_SERVICE` unless you restate those two lines. For more control, register an **`HttpCodeStatusMapper`** bean.

```properties
management.endpoint.health.show-details=always
management.endpoint.health.show-components=always
```

**Listing 2.** Values: `never` (default for **show-details**), `when-authorized`, `always`. If **show-components** is unset, it follows **show-details**. `when-authorized` uses `management.endpoint.health.roles` (empty ⇒ any authenticated user).

```d2
direction: right
leaves: "HealthIndicators\ndb, disk, ping, custom" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
agg: "StatusAggregator\norder: DOWN, OUT_OF_SERVICE,\nUP, UNKNOWN" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
http: "HTTP 503 if DOWN / OOS\nHTTP 200 if UP / UNKNOWN" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

leaves -> agg -> http
```

**Fig. 1.** One **`DOWN`** leaf makes the **root** **`DOWN`** and the HTTP status **503**. Health **groups** (`management.endpoint.health.group.<name>.include` / `exclude`) can use their own `status.order` and `http-mapping` ([[Which Actuator endpoints are exposed over HTTP by default]]).

The JSON body is only `{ "status": "…" }` until details/components are shown. The endpoint still must be **exposed** ([[How do you expose Spring Boot Actuator endpoints safely]]). Reactive apps use **`ReactiveHealthContributor`**; blocking indicators run on the elastic scheduler.

> [!warning] Default JSON hides the tree
> **`show-details`** defaults to **`never`**, so probes and browsers see **only** the aggregate status. A single failing indicator still flips that status to **`DOWN`** even when you cannot see **which** one. `always` on a secured app also needs the security chain to **permit** `/actuator/health` for the callers you care about.

> [!warning] Unknown codes look healthy over HTTP
> A custom `Status` missing from **`status.order`** does not compete in the sort. **`UNKNOWN`** (and any other **unmapped** code, including **`UP`**) is HTTP **200**. Putting `FATAL` in **`http-mapping`** without restating **`down`** and **`out-of-service`** drops the default **503** mappings.

> [!tip] Interview answer
> Actuator aggregates HealthIndicator statuses with a StatusAggregator that sorts against status.order and takes the first, defaulting to DOWN then OUT_OF_SERVICE then UP then UNKNOWN. That is why one DOWN database indicator makes /actuator/health return DOWN and HTTP 503. The body still hides per-indicator details until I set show-details, and UNKNOWN still maps to 200.
