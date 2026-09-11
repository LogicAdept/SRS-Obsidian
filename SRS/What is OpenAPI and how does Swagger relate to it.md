<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is OpenAPI and how does Swagger relate to it

> [!abstract] Short answer
> OpenAPI is the vendor-neutral specification for describing HTTP APIs — a machine-readable document listing endpoints, methods, parameters, schemas, and responses (current version 3.1, aligned with JSON Schema). Swagger is the former name of the spec (renamed OpenAPI when it moved to the OpenAPI Initiative in 2016) and today the brand of the original tooling — Swagger UI, Swagger Editor, Swagger Codegen lineage — that reads such documents.

## What the document gives you

An OpenAPI document is a JSON/YAML description of the contract: servers, paths, per-method operations with parameters and request bodies, response schemas per status, reusable components (schemas, security schemes), and metadata. From that single artifact the ecosystem derives: interactive documentation (Swagger UI renders it into a clickable console), client SDKs in dozens of languages (OpenAPI Generator), server stubs, mock servers for consumers before the backend exists, and CI checks — spec diffs catch breaking changes ([[What changes are breaking for a REST API]]), and generated interfaces pin implementations ([[What is the difference between contract-first and code-first API development]]). Security schemes (bearer, OAuth2 flows, API keys) document auth without binding you to an enforcement library. 3.1's JSON Schema alignment matters practically: the same schema vocabulary describes request validation, examples, and even non-HTTP event payloads, so one modeling language spans artifacts.

```d2
doc: OpenAPI document (YAML/JSON)
doc.ui: Swagger UI
interactive docs
doc.sdk: client SDKs
(OpenAPI Generator)
doc.stub: server stubs
doc.mock: mock server
doc.ci: CI diff
(breaking-change gate)
tool: Swagger tooling family {
  ui2: Swagger UI (reader)
  ed: Swagger Editor (author)
}
doc.ui -> tool.ui2
doc.ed -> doc: authors
doc -> doc.sdk
doc -> doc.stub
doc -> doc.mock
doc -> doc.ci
```

**Fig. 1.** One artifact, many derivations: docs, SDKs, stubs, mocks, and CI gates all read the same document.

## The name tangle, handled cleanly

History: the spec began as Swagger (SmartBear, 2011), was donated in 2015/2016 to the Linux Foundation's OpenAPI Initiative and renamed OpenAPI Specification; Swagger remained SmartBear's tooling brand. So today: "an OpenAPI document" is the artifact; "Swagger UI" is a viewer for it; "Swagger" alone usually means the tools or the legacy name. Interviewers probe exactly this and the practical corollary — springdoc-openapi generates OpenAPI 3 documents at runtime for Spring apps and serves them through Swagger UI ([[What is Spring Data REST]] exposes HAL plus a browsable API in the same spirit), so a code-first team still ships the artifact. Version pinning matters: 2.0 (Swagger) versus 3.0 versus 3.1 documents differ structurally, and generators handle them unevenly ([[What is API-first design]] makes the document the process centerpiece rather than an afterthought).

```yaml
openapi: 3.1.0
info: {title: Orders API, version: 2.0.0}
paths:
  /orders/{id}:
    get:
      parameters:
        - {name: id, in: path, required: true, schema: {type: integer}}
      responses:
        "200":
          content:
            application/json:
              schema: {$ref: "#/components/schemas/Order"}
        "404":
          content:
            application/problem+json: {}
components:
  schemas:
    Order:
      type: object
      required: [id, status]
      properties:
        id: {type: integer}
        status: {type: string, enum: [NEW, PAID, CANCELLED]}
```

**Listing 1.** A minimal OpenAPI 3.1 fragment: path, parameter, per-status responses, and a reusable schema component (conceptual, per the OpenAPI 3.1 specification structure).

> [!warning] A generated document is not a designed contract
> Runtime-generated OpenAPI from controllers describes implementation accidents as faithfully as decisions — including the fields you did not mean to publish. Review and pin the artifact; otherwise the ecosystem's SDKs and mocks faithfully reproduce your leaks.

> [!tip] Interview answer
> OpenAPI is the vendor-neutral spec for describing HTTP APIs — endpoints, schemas, responses, security — currently 3.1, JSON Schema aligned. Swagger is both its old name and the tooling brand: Swagger UI renders the document into an interactive console. One artifact yields docs, SDKs, mocks, and CI breaking-change diffs, which is why it anchors contract-first work. Spring's springdoc generates it at runtime and serves it via Swagger UI.
