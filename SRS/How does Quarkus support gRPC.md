<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How does Quarkus support gRPC

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: quarkus-grpc generates stubs from .proto at build time (grpc-java + protobuf plugins), registers services as beans, serves over Vert.x HTTP with plain or TLS, supports Mutiny stubs (Uni/Multi) and blocking stubs; reflection-free and native-friendly.
