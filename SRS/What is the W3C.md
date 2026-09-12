<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS
# What is the W3C

> [!abstract] Short answer
> The W3C (World Wide Web Consortium) is the international standards organization founded by Tim Berners-Lee in 1994 to keep the web interoperable: it develops and publishes web standards — HTML and CSS historically, accessibility (WCAG), internationalization, XML-family technologies — through a consensus process of member organizations, staff and public review. Today HTML spec work is led jointly with the WHATWG, while W3C runs review, ratification (W3C Recommendations) and the wider horizontal policies (privacy, accessibility).

## What the W3C actually produces

1. **Recommendations** — the formal name of its standards (CSS specifications, WCAG accessibility guidelines, WebRTC, WebAssembly API bindings...). The process is Working Draft → Candidate Recommendation → Recommendation, with public drafts and test suites.
2. **Horizontal specifications** — cross-cutting concerns: accessibility (WCAG — the legal basis of many accessibility laws), internationalization (encodings, bidi text), privacy principles.
3. **Groups and community processes** — members (companies, universities), working groups, community groups; specifications are developed in the open, on GitHub these days.

```d2
direction: right
members: "Members + staff\n+ public input" { width: 240; height: 80; style.fill: "#e3f2fd" }
wg: "Working group\ndrafts the spec" { width: 230; height: 80; style.fill: "#fff3e0" }
rec: "W3C Recommendation\n(tested, ratified)" { width: 260; height: 80; style.fill: "#e8f5e9" }
impl: "Browsers implement\ninteroperability" { width: 250; height: 80; style.fill: "#e8f5e9" }
members -> wg -> rec -> impl
impl -> wg: "issues, test results"
```

**Fig. 1.** The standards loop: consensus drafting, ratification, implementation feedback.

## How it fits among the other bodies

The web's governance is split: **WHATWG** maintains the living HTML/DOM/URL standards (since the 2019 agreement W3C publishes the HTML Recommendation in sync with WHATWG's review draft); **IETF** standardizes HTTP and URI; **ECMA International** standardizes JavaScript (ECMAScript); **Unicode Consortium** owns the character tables; W3C holds the umbrella role for the platform's cross-cutting quality bars. Knowing who owns what is the actual interview point: "who defines HTML?" — WHATWG; "who defined WCAG?" — W3C.

> [!warning] W3C does not enforce anything and does not own the web
> Recommendations are vendor-implemented: a "standard" only works if browsers ship it (the reason "W3C validated my page" means little about rendering). And the historical drama — the XHTML-era "HTML is dead" detour and the HTML5 split that created WHATWG — explains why two bodies share the stack today. Claiming "W3C controls JavaScript" confuses ECMA (language) with W3C (platform APIs).

Context: [[What is the World Wide Web]] for what this consortium stewards, [[What is a web server]] / [[What is a web application]] for where standards meet deployments, [[What is a MIME type]] for the format registry side (IANA, not W3C).

> [!tip] Interview answer
> The W3C is the web's standards consortium, founded by Berners-Lee in 1994 — it ratifies Recommendations like CSS, WCAG accessibility and internationalization through an open consensus process. The nuance I add: HTML now comes from WHATWG's living standard with W3C publishing the snapshot, HTTP belongs to the IETF, and JavaScript to Ecma — the W3C is the platform's umbrella, not its monarch.
