<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> GraphQL's protocol sends JSON, and JSON does not carry binary — so uploads use the **multipart request spec**: the client POSTs `multipart/form-data` with two form fields — `operations` (the GraphQL document with a placeholder where the file goes) and `map` (which file part fills which placeholder path). The server parses the multipart body, binds the file into the variables, and hands a `Upload`-style scalar to the resolver, which streams it to storage. Files never travel inside the GraphQL JSON.

## The multipart mapping, step by step

The spec fixes the shape. `operations` holds the normal `{query, variables, operationName}` payload, but file positions in `variables` are `null` placeholders. `map` is `{"0": ["variables.file"]}` — part `0` fills that path. Each subsequent part (`0`, `1`, ...) is the raw binary. The server resolves placeholders **before** validation/coercion, so the schema declares the field with a custom `Upload` scalar and the resolver receives a stream handle, not bytes-in-memory ([[What are GraphQL scalar types]]).

```text
# POST /graphql   Content-Type: multipart/form-data; boundary=----
# form field "operations":
#   { "query": "mutation ($file: Upload!) { uploadFile(file: $file) { id size } }",
#     "variables": { "file": null } }
# form field "map":
#   { "0": ["variables.file"] }
# form field "0":  <raw binary part>
# server binds part 0 into variables.file, then executes normally.
```

**Listing 1.** The two-level indirection — operations + map — is what lets one request carry several files bound to arbitrary variable paths, including inside lists ([[Why do GraphQL mutations use input types instead of object types]]).

```d2
direction: down
M: "multipart/form-data" { width: 230; height: 55 }
O: "operations: query +\nvariables.file = null" { width: 300; height: 65 }
Mp: "map: 0 -> variables.file" { width: 260; height: 60 }
B: "server binds parts into variables" { width: 320; height: 60 }
R: "resolver: Upload scalar ->\nstream to storage" { width: 310; height: 65 }
M -> O
M -> Mp
O -> B
Mp -> B
B -> R
```

**Fig. 1.** The multipart envelope surrounds ordinary GraphQL execution; binding happens before validation, so the resolver sees a typed file handle.

> [!warning] Uploads are a convention layered on transports — not a GraphQL feature
> First: the multipart request spec is a **community convention** (widely implemented by servers and clients), not part of the GraphQL spec — plain "GraphQL over HTTP" with JSON does not carry files, and a server without multipart support simply cannot accept uploads, whatever its schema says ([[What is GraphQL introspection]]). Second: do not fall back to Base64 strings inside variables "because it works": it inflates payloads by ~33%, defeats streaming (the whole body must exist in memory), and skews every cost/limit mechanism — multipart exists precisely to avoid this ([[Why is rate limiting harder in GraphQL than REST]]). Third: the `Upload` scalar is **input-only**: it never appears in responses, and it must be wired per server implementation — SDL alone declares nothing executable ([[What is Schema Definition Language in GraphQL]]).

Operational notes: validation of size/type belongs in the resolver or middleware before streaming (multipart parts arrive with sizes; reject early), antivirus/scan steps sit between binding and storage, and upload mutations should return small payload types (`id`, `size`, url) rather than echoing the file. Streaming from part to object storage without full buffering is the default expectation for large files ([[What does the GraphQL errors array contain]]).

> [!tip] Interview answer
> Files ride a multipart/form-data envelope around the GraphQL request: the operations field carries the document with null placeholders in variables, and a map field binds each binary part to a variable path. The server substitutes parts before execution, so an input-only Upload scalar delivers a stream to the resolver. It is a community spec, not core GraphQL — and Base64-in-JSON is the anti-pattern it exists to avoid.

