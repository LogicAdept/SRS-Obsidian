<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI #Patterns/Architecture/Microservices/UIComposition #SRS

# How would you explain server side page fragment composition

> [!abstract] Short answer
> Server-side page fragment composition builds pages that span microservices on the server: each team owns a service that renders the HTML fragment for its region of the page (header, product panel, recommendations), and a template layer aggregates the fragments into the final page before it is sent to the browser. It is the UI-side counterpart of client-side composition; the browser sees one server-rendered page.

## The mechanics: template plus per-team fragments

The pattern splits a page vertically along service boundaries. Each team's service renders its fragment — complete, styled HTML for its region — and exposes it at a URL or template partial. The page template (owned by a UI/core team) declares the layout and the fragment sources; the server-side aggregation stitches fragments into the final document (classic server-side includes, edge-side includes like ESI, or a modern rendering proxy). The browser gets one page, one origin, no client orchestration. This is the natural fit when teams own both a service and its UI region — the same team boundary as the underlying data ([[How would you explain the database per service pattern]] makes each team's data private; fragment composition makes each team's UI region private too).

```d2
direction: down
req: "GET /product/100" {style.fill: "#eceff1"}
layout: "Layout / template
declares regions" {style.fill: "#fff3e0"}
h: "Header service
renders <header>" {style.fill: "#e8f5e9"}
p: "Product service
renders <section>" {style.fill: "#e8f5e9"}
r: "Recommendations service
renders <aside>" {style.fill: "#e8f5e9"}
out: "One composed HTML page" {style.fill: "#f3e5f5"}
req -> layout
layout -> h: fetch fragment
layout -> p: fetch fragment
layout -> r: fetch fragment
h -> out
p -> out
r -> out
```

**Fig. 1.** Three teams, three fragments, one server-rendered page; the template owns layout, teams own content.

## Trade-offs versus the client-side alternative

Benefits: performance and simplicity on the client — no framework bootstrap, no client-side routing for composition, fast first paint; SEO works by construction; and a fragment failing can degrade just its region (render a placeholder, keep the page). Costs: the aggregation layer is critical shared infrastructure (it must be fast, cache fragments aggressively, and bound per-fragment timeouts — the same composer-availability math as [[What is the API composition pattern in microservices]] applies to HTML); consistency of styling and shared client behavior across fragments needs governance (shared design system); and interactive state that crosses regions (cart badge updating when a fragment's button is clicked) is awkward in pure server rendering. The client-side counterpart moves composition into the browser — each team ships a JavaScript component and the shell assembles them ([[How would you explain client side UI composition for micro frontends]]); micro-frontend architectures combine both per page and per requirement ([[What is the API gateway pattern in microservices]] remains the data-plane edge for both styles).

> [!warning] Fragment latency is page latency — until you isolate it
> Server-side stitching serializes whatever it does not parallelize: three fragments fetched sequentially cost the sum, and one slow team's fragment delays every page that includes it. The pattern demands parallel fetch, per-fragment timeouts with placeholder fallbacks, and aggressive caching — otherwise the slowest team sets the site's response time.

> [!tip] Interview answer
> Server-side fragment composition: each team's service renders the HTML for its region of the page, and a template layer stitches the fragments server-side, so the browser receives one page. I get fast first paint, SEO by construction and per-team regions, at the cost of a critical aggregation layer that needs parallel fetch, timeouts and placeholder degradation. Interactive cross-region state is where it gets awkward — that's when I move regions to client-side composition or a hybrid.
