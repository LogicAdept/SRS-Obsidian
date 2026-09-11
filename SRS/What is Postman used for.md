<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is Postman used for

> [!abstract] Short answer
> Postman is an API development and testing platform: its core is a client for composing and sending HTTP requests, organized into collections with environments, variables, and scripted request chains. Around that core sit automated test runs (Newman), mock servers, documentation, and team workspaces — covering the explore-test-document loop of API work.

## The request client and the scripted chain

Day-to-day: build a request (method, URL, headers, body), save it into a collection, and parameterize values through environments — {{baseUrl}}, {{token}} — so the same collection runs against dev, staging, and production. The chain feature is what interviewers mean by "knowing Postman": pre-request scripts compute signatures or fetch tokens (pm.environment.set to store an accessToken from the login response), and Tests scripts assert on responses (pm.response.code, pm.expect) and chain values into subsequent requests. Collections become executable documentation of a flow — login, create, verify, cleanup — reviewable in version control (collections are JSON) ([[What are the key principles of good API design]] — a collection is a consumability check of your API). The platform layer: Newman runs collections headless in CI; mock servers serve responses from an OpenAPI document or examples; documentation renders from collections; workspaces share all of it ([[What is OpenAPI and how does Swagger relate to it]] — Postman imports and publishes OpenAPI).

```text
1) POST /auth/login -> save: pm.environment.set("token", ...)
2) GET /users/me, Authorization: Bearer {{token}} -> 200
3) assert: pm.expect(pm.response.code).to.eql(200)
4) run whole flow headless: newman run collection.json -e env.json
```

**Listing 1.** The scripted-chain shape: environment variables carry the token between requests; assertions live with each request; Newman replays the flow in CI (conceptual, per Postman Learning Center).

## Where it sits in a team's toolkit

Postman covers the human-driving-calls niche: API exploration during development, smoke and integration flows without writing harness code, contract walkthroughs with consumers, and CI regression via Newman when the flows are stable. It does not replace unit tests or property-based testing; complex logic lives awkwardly in its scripting sandbox, and heavy use pushes you toward dedicated test code ([[What is REST Assured]] for in-process Java assertions in the same niche; [[How do you test the service layer in Spring]] for the layer below; [[What is TestRestTemplate]] for Boot-flavored integration tests). The collaboration features (workspaces, versioned collections, public API network) make it the de-facto shared folder of request knowledge — the reason interviewers ask about it is less the tool than the workflow maturity it signals: parameterized environments over hardcoded URLs, chained flows over single calls.

```d2
col: collection (saved requests)
env: environment {{baseUrl}} {{token}}
pre: pre-request script
(fetch token, sign)
send: send request
test: Tests script
assert + save values
next: next request uses {{token}}
col -> send
env -> send
pre -> send
send -> test
test -> next
```

**Fig. 1.** The Postman loop: parameterized request, scripted pre-processing, assertions that chain values into the next call.

> [!warning] Postman collections are not a test suite
> Collections with a few status-code assertions give false confidence: they exercise happy paths, not contracts. Real regression coverage lives in code (JUnit + Testcontainers or equivalent); treat collections as exploration, onboarding, and CI smoke flows.

> [!tip] Interview answer
> Postman is my API workbench: requests grouped in collections, environments with variables so the same flow hits dev or staging, pre-request scripts to fetch tokens and Tests to assert and chain values. Collections double as living documentation, Newman runs them headless in CI, and the platform adds mocks and docs from OpenAPI. I use it for exploration and smoke flows — the regression suite proper lives in code.
