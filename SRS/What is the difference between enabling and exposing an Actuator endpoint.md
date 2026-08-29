<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# What is the difference between enabling and exposing an Actuator endpoint?

> [!abstract] Short answer
> **Access** (interview dumps still say **enabled**) is whether the endpoint’s operations are permitted: `none`, `read-only`, or `unrestricted`. **Exposure** is whether a **transport** publishes it — HTTP (`management.endpoints.web.exposure.include` / `exclude`) or JMX. An endpoint is **available** only when **both** match (`@ConditionalOnAvailableEndpoint`); then Boot auto-configures the bean. Default: access is **unrestricted** except **`shutdown`** and **`heapdump`**; only **`health`** is exposed over HTTP **and** JMX.

## Two knobs, then a bean

`Access` values: **`NONE`** (no operations), **`READ_ONLY`** (`@ReadOperation` / GET+HEAD), **`UNRESTRICTED`**. Set one endpoint with `management.endpoint.<id>.access`. Opt-in for everything with `management.endpoints.access.default=none`, then raise individuals. `management.endpoints.access.max-permitted` **caps** every endpoint (`none` or `read-only` beat a looser per-id value).

Interview dumps use `management.endpoint.<id>.enabled` and `management.endpoints.enabled-by-default`. Those still resolve through `PropertiesEndpointAccessResolver` and are **deprecated** in favor of the `access` properties.

```properties
management.endpoints.access.default=none
management.endpoint.loggers.access=read-only
```

**Listing 1.** Opt-in access: only `loggers`, and only **reads**. Inaccessible endpoints are **removed from the context**. This is **not** an exposure list ([[How do you change log levels at runtime with Actuator]]).

```properties
management.endpoints.web.exposure.include=health,info
```

**Listing 2.** HTTP exposure. Defaults: **`include=health`** on **web and JMX**; `exclude` **wins** over `include`. `*` means all IDs ([[Which Actuator endpoints are exposed over HTTP by default]]).

```properties
management.endpoints.web.exposure.include=*
management.endpoints.web.exposure.exclude=env,beans
```

**Listing 3.** Expose every HTTP endpoint except `env` and `beans`. Quote `"*"` in YAML (`*` is a YAML alias).

```d2
direction: down
access: "access\nnone / read-only / unrestricted" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
expose: "exposure\nweb.include / jmx.include" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
avail: "@ConditionalOnAvailableEndpoint\navailable = access AND exposed" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
http: "/actuator/{id}\nstill may be secured" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}

access -> avail
expose -> avail
avail -> http
```

**Fig. 1.** Dumps that say “enabled ⇒ the bean exists” skip the second gate: no exposure on **any** technology means the built-in endpoint is **not** auto-configured.

> [!warning] Access is not exposure
> `management.endpoints.access.default=none` (or the deprecated `enabled-by-default=false`) does **not** change include/exclude. `include=loggers` does **not** raise `read-only` to `unrestricted`. Mixing the two is the usual Actuator miss. Security is a **third** gate: with Spring Security on the classpath and no custom `SecurityFilterChain`, every actuator **other than** `/health` is secured ([[How do you expose Spring Boot Actuator endpoints safely]]).

> [!warning] Boot 4 JMX is not “everything”
> Older Boot exposed **all** enabled endpoints over **JMX** by default. Current defaults match HTTP: **`health` only**. `conditions` is typically **on** (unrestricted access) and still **404** until you include it ([[How can you debug which auto-configuration classes applied]]).

> [!tip] Interview answer
> Enabled — now access — is whether the endpoint may run: none, read-only, or unrestricted. Exposed is whether HTTP or JMX actually publishes it; default web and JMX include is health only. Boot auto-configures the bean only when both are true. Dumps still say management.endpoint.id.enabled; on current Boot that property is deprecated in favor of management.endpoint.id.access.
