<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `VirtualFilterChain` in Spring Security?

> [!abstract] Short answer
> A **private** `FilterChain` inside [[What is FilterChainProxy and DelegatingFilterProxy]]. After a [[What is SecurityFilterChain]] matches, `FilterChainProxy` does **not** register those filters with the servlet container. It wraps `chain.getFilters()` in **`VirtualFilterChain`**, which calls each security `Filter` with **itself** as the next chain, then — when the list is done — calls the **original** servlet `FilterChain` (toward `DispatcherServlet`). TRACE **`Invoking SomeFilter (n/m)`** is this loop.

## Security filters are not Tomcat filters

```d2
direction: down
dfp: "DelegatingFilterProxy\nspringSecurityFilterChain" {
  width: 280
  height: 50
}
vfc: "VirtualFilterChain\nadditionalFilters + originalChain" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
sec: "HeaderWriter … AuthorizationFilter" {
  width: 280
  height: 40
}
ds: "original FilterChain\nDispatcherServlet" {
  width: 240
  height: 50
}

dfp -> vfc
vfc -> sec: "n/m"
vfc -> ds: "position == size"
```

**Fig. 1.** `FilterChainProxy` javadoc: do **not** list the Security filters in `web.xml`. `setFilterChainDecorator` (since **6.0**): by default it “decorates the filter chain with a `VirtualFilterChain` that iterates through security filters and then delegates to the original chain.” Public wrapper: `VirtualFilterChainDecorator`. See [[What is the springSecurityFilterChain bean name]] and [[What happens if no SecurityFilterChain matches a request]] (empty/no match skips the extra list and continues the original chain).

A security filter that **never** calls `chain.doFilter` stops both the rest of Security **and** the servlet. That is the same contract as any `Filter`.

```text
TRACE FilterChainProxy : Invoking SecurityContextHolderFilter (3/15)
TRACE FilterChainProxy : Invoking HeaderWriterFilter (4/15)
```

**Listing 1.** Logged from `VirtualFilterChain.doFilter` (`currentPosition` / `size`). Architecture: put a breakpoint on `FilterChainProxy` first — this inner class is what actually walks `getFilters()`. Observation (when on) may wrap the same idea as `ObservationFilterChainDecorator$VirtualFilterChain`. See [[How do you enable Spring Security debug logging for the filter chain]].

> [!warning] Private type, public behavior
> Do not inject `VirtualFilterChain`. You only meet it on a **stack trace**. `addFilterBefore` still inserts into the **`SecurityFilterChain` list**, not into Tomcat. If TRACE never prints `Invoking`, this request never entered a non-empty virtual chain.

> [!tip] Interview answer
> VirtualFilterChain is FilterChainProxy’s inner FilterChain. Security filters are not registered with the servlet container; the proxy runs them on this virtual chain and then continues the original chain to the DispatcherServlet. The TRACE line Invoking FilterName (n of m) is that loop. Debug FilterChainProxy first because that is where the virtual chain starts.
