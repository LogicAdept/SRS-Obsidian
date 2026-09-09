<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How does Quarkus generate OpenAPI documentation

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: quarkus-smallrye-openapi generates /q/openapi schema from Jakarta REST annotations at build time; swagger-ui extension serves interactive UI in dev/test; annotations @Operation/@Schema enrich the model; static openapi.yaml possible.
