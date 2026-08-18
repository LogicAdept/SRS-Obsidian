<!--
reps: 0
priority: 0
-->
#API/GraphQL #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

REST: cache by URL because each endpoint has a stable shape. GraphQL: many operations share one URL (often POST `/graphql`) and the body chooses fields, so CDN/HTTP caches keyed on URL do not see a stable resource.

Dumps move caching to: client normalized caches (Apollo/Relay, objects by type+id); server/resolver caches; persisted queries + GET so a hash is cacheable. Server-side 'cache the GraphQL response like REST' is called a poor fit because the next client may ask a different shape.

> [!warning] Unverified traps from the dump
> - Dump claim: GraphQL trades REST HTTP caching for a normalized client cache keyed by identity.
