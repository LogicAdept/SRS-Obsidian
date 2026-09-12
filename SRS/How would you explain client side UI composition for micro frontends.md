<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI/MicroFrontends #Patterns/Architecture/Microservices/UIComposition #SRS

# How would you explain client side UI composition for micro frontends

> [!abstract] Short answer
> Client-side UI composition for micro-frontends assembles the page in the browser: each team ships a self-contained frontend component (its own build, its own framework version, its own release), and a shell application composes these components into pages at runtime — decoupling frontend teams the way microservices decouple backend teams. Client-side and server-side page fragment composition form the pattern pair.

## The mechanics: shell, components, contracts

Three parts. The shell (container) owns the frame: routing between pages, global concerns (authentication session, design tokens, shared state), and the composition points — it decides which team's component renders in each region and mounts it (runtime integration via JavaScript modules, custom elements/Web Components, or module federation style sharing). Each team's component is a vertical slice: markup, styles, logic and its own data calls against its own backend (or its BFF, [[How would you explain the backends for frontends pattern]]) — built and released independently. The contract between shell and components is deliberately thin: custom-element or framework-agnostic boundaries, defined styling scoping (shadow DOM or naming conventions), and a small cross-component API (routing events, shared context) — The central advice is to minimize cross-component communication, because every shared channel re-couples the teams.

```d2
direction: down
shell: "Shell
routing, auth, design tokens" {style.fill: "#fff3e0"}
c1: "Team A: product page
own build + release" {style.fill: "#e8f5e9"}
c2: "Team B: buy box
own build + release" {style.fill: "#e8f5e9"}
c3: "Team C: reviews
own build + release" {style.fill: "#e8f5e9"}
b1: "Product API" {shape: cylinder; style.fill: "#eceff1"}
b2: "Pricing API" {shape: cylinder; style.fill: "#eceff1"}
shell -> c1: mount
shell -> c2: mount
shell -> c3: mount
c1 -> b1
c2 -> b2
```

**Fig. 1.** The shell mounts team-owned vertical slices; each slice owns its data path end to end.

## Trade-offs versus server-side composition — and the costs either way

Strengths: true independent deployability of UI slices (a team ships its region without a page release); framework diversity becomes possible (per-team React/Vue/ce-once choices — an advantage that is best not used); rich client-side interactivity across mounts without full page reloads; and SPA-style UX preserved. Costs: bundle size and duplication (three teams' framework runtimes in one page without care), styling conflicts and design drift (mitigated by a design system and scoped styles), more complex end-to-end testing (integration happens at runtime, in browsers), first-paint performance needs engineering (lazy mounts, prefetching), and the shell itself is critical shared infrastructure with its own release discipline. This is the client-side counterpart of server-side fragment stitching ([[How would you explain server side page fragment composition]]) — the two patterns differ in where composition happens and which trade each pays; the data-layer plumbing behind both is the same gateway/BFF landscape ([[What is the API gateway pattern in microservices]]). The adoption test: micro-frontends buy organization-scale benefits — many frontend teams shipping independently — and are overhead for small teams; the same verdict as microservices themselves ([[What advantages do microservices have over a monolith]] is the backend mirror).

> [!warning] The composition boundary is an API — treat it like one
> A shell mounting team components shares runtime process space: one component's global style leak, polluted prototype or unhandled error is every region's problem. Version incompatibilities between shell and components appear exactly like breaking API changes — and need the same discipline: versioned contracts, compatibility windows, and integration tests across at least the current shell with each supported component version.

> [!tip] Interview answer
> Client-side composition is the micro-frontend style where a shell app mounts each team's self-contained component in the browser — routing, auth and design tokens in the shell; each slice owns its markup, logic and data path, built and released independently. I get real per-team deployability and SPA interactivity, paying in bundle duplication, styling governance, runtime integration testing and shell criticality. It's the client-side twin of server-side fragment composition — and like microservices, it pays only at the scale of several frontend teams.
