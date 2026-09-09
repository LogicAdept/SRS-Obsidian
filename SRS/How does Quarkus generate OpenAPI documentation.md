<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus generate OpenAPI documentation?

> [!abstract] Short answer
> The `quarkus-smallrye-openapi` extension builds an **OpenAPI schema from the application's Jakarta REST annotations during augmentation** and serves it at **`/q/openapi`** (YAML by default, `?format=json`); the companion `quarkus-swagger-ui` extension serves an interactive UI that consumes that schema in dev and test mode. Enrichment uses SmallRye OpenAPI annotations (`@Operation`, `@Schema`, `@ApiResponse`) or a static `openapi.yaml` resource merged into the model — no separate doc build step, and the schema cannot drift from the code it describes.

## From annotations to a served schema

At build time the extension reads the Jandex index of REST resources, derives paths, methods, parameters, status codes and media types, and produces the document the runtime serves ([[What is Jandex in Quarkus]]). Because derivation happens from the same compiled annotations the runtime dispatches on, the contract follows the code mechanically — adding a resource method changes the schema on the next build. Programmatic enrichment: SmallRye annotations on classes/methods add descriptions, examples, security requirements; a static `META-INF/openapi.yaml` merges with the generated model (static wins where both define a node), which is how teams pin hand-written descriptions while keeping generated paths. Configuration knobs: `quarkus.smallrye-openapi.path` moves the endpoint, `mp.openapi.model.format`, info/description properties.

```java
// The verified app served both endpoints (JDK 21, Quarkus 3.39.2; smallrye-openapi on the
// classpath). Resource and generated output, condensed:
package org.acme.check;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/echo")
public class EchoResource {
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String echo(@QueryParam("q") String q) {
        return "echo:" + q;
    }
}
// GET /q/openapi (verbatim fragment of the produced document):
//   /demo/echo:
//     get:
//       parameters:
//       - name: q
//         in: query
//         schema: { type: string }
//       responses:
//         "200":
//           description: OK
// The paths /demo/* and /echo/* appeared without any OpenAPI annotation in the sources.
```

**Listing 1.** A no-annotation resource still produced a complete path entry — derivation comes from `@Path`/`@GET`/`@QueryParam` themselves. The Swagger UI page (dev mode) is just a renderer for this same document.

```d2
direction: down
src: "Jakarta REST resources\n@Path, @GET, @QueryParam" {
  width: 290
  height: 60
}
aug: "Augmentation (smallrye-openapi)\nderive schema from index" {
  width: 320
  height: 65
  style.fill: "#fff3e0"
}
static: "META-INF/openapi.yaml\noptional static merge" {
  width: 280
  height: 60
  style.fill: "#f5f5f5"
}
doc: "OpenAPI 3 document" {
  width: 230
  height: 50
  style.fill: "#e3f2fd"
}
ui: "Swagger UI (dev/test)\n/q/swagger-ui" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
ep: "/q/openapi\nYAML | ?format=json" {
  width: 240
  height: 55
}
src -> aug -> doc
static -> doc
doc -> ep -> ui
```

**Fig. 1.** One generated document feeds both the raw endpoint and the UI; static resources merge in but the generated paths remain code-driven ([[How do you test a Quarkus application]] uses the same resources).

## Contract-first vs annotation-first

The supported workflow is annotation-first with optional static merge; full contract-first (code generated from an OpenAPI file) is a different toolchain. For teams exposing public APIs, the usual additions are security schemes (mapping onto the OIDC bearer setup) and server entries per environment — both expressible in the merged static document or config.

> [!warning] The schema exists, that does not mean it is a good contract
> Derived documents carry real signatures but no semantics: parameter descriptions, error models and examples are empty unless you enrich them — reviewers mistake "the endpoint is documented" for "the contract is complete". Two operational traps: Swagger UI defaults to dev/test — enabling it in prod publishes your API surface (either keep it off or protect it), and renaming a resource field changes the schema silently, breaking consumers who pinned to the previous document — the schema is generated, it is not automatically versioned.

> [!tip] Interview answer
> Quarkus derives the OpenAPI document at build time with smallrye-openapi: it reads the REST annotations from the class index and serves the result at /q/openapi — YAML or JSON — with the Swagger UI extension rendering it in dev mode. I enrich with @Operation and @Schema annotations or merge a static openapi.yaml, and because derivation comes from the same annotations the runtime uses, the doc cannot drift from the code. Verified in my demo: even an unannotated resource produced complete path entries.
