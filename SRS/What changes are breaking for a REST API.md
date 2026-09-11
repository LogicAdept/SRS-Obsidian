<!--
reps: 0
priority: 0
-->
#API/Contracts #API/REST #SRS

# What changes are breaking for a REST API

> [!abstract] Short answer
> A change is breaking when a previously correct client can fail because of it: removing or renaming fields and endpoints, changing types or value ranges, altering status-code or error contracts, adding required request input, tightening validation, or changing documented semantics. Adding optional output, new endpoints, and new optional parameters is non-breaking — with a few famous gray zones.

## The classification clients depend on

Walk the wire: request side — removing/renaming request fields, adding a required field, rejecting inputs you previously accepted (tighter validation), changing a parameter's meaning are breaking; new optional parameters and new endpoints are not. Response side — removing or renaming response fields (clients that read them break), changing a field's type (number -> string) or nullability, changing which status codes a call can return (a call that could 404 becoming 200-only, or errors changing classes), changing error type codes, and semantic flips (same shape, different meaning — "active" starts including archived) are all breaking. URI and transport: removing or redirecting endpoints, changing auth schemes, removing a supported content type ([[What is content negotiation in REST APIs]]) — breaking. The gray zones everyone should name: adding enum values or new error codes (breaks exhaustive switches — lenient clients tolerate, strict ones crash), adding fields (breaks clients with strict deserialization like closed-schema codegen or Java records with unknown-field errors), and pagination default changes ([[What is the difference between offset and cursor pagination]]).

```d2
add: additive (safe) {
  a1: new optional response fields
  a2: new endpoints
  a3: new optional request params
}
brk: breaking (new version) {
  b1: remove/rename fields
or endpoints
  b2: type/nullability changes
  b3: required request input
  b4: tighter validation
  b5: status/error contract change
  b6: semantic flips
}
gray: gray zones (document!) {
  g1: new enum values
  g2: new error codes
  g3: strict clients vs new fields
}
add -> gray: strict deserializers
gray -> brk: strict clients crash
```

**Fig. 1.** The three buckets: additive, breaking, and the documented gray zone that behaves differently per client strictness.

## Governance for a moving API

The practical machinery: a compatibility contract in the style guide (which side of each gray zone the API takes — e.g. "new enum values are breaking here"), a consumer-driven contract test suite that replays real recorded traffic against proposed changes (the only test that catches "a field our biggest client depends on but nobody documented"), OpenAPI diffing in CI so a breaking edit cannot merge unnoticed ([[What is OpenAPI and how does Swagger relate to it]] for the machine-readable side; [[What are the key principles of good API design]] for the consistency discipline), deprecation headers and Sunset dates before removal ([[How should you version a public API]] for the ladder), and response projections that stop raw entities from leaking — an entity refactor silently becomes a public break otherwise. Compatibility is one-way in practice: never remove; make it optional, then deprecated, then dead.

```text
additive (safe)      : new optional fields, new endpoints, new params
breaking (new version): remove/rename fields or endpoints, type changes,
                       required request input, tighter validation,
                       status/error contract changes, semantic flips
gray (document it)   : new enum values (exhaustive switches),
                       new error codes, strict deserializers vs new fields
```

**Listing 1.** The classification clients rely on, with the gray zone made explicit instead of argued per incident (conceptual).

> [!warning] "Just adding a field" breaks strict clients
> Codegen with closed schemas, Java records mapped with unknown-field failures, and statically typed SDKs can turn your harmless new response member into a deserialization error. Additive is a contract about your docs; the client's parser policy decides the truth — which is why the style guide must fix the gray zones.

> [!tip] Interview answer
> Breaking is anything that can fail a previously correct client: removing or renaming fields and endpoints, changing types, nullability, status or error contracts, adding required input, tightening validation, or flipping semantics. Additive — new optional fields, endpoints, parameters — is safe, with gray zones I call out: new enum values break exhaustive switches, new fields break strict deserializers. I enforce this with OpenAPI diffs and recorded-traffic contract tests, and deprecate with dates instead of removing.
