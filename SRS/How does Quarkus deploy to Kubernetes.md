<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How does Quarkus deploy to Kubernetes

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: quarkus-kubernetes generates manifests (Deployment, Service) at build time; container-image extensions (docker/jib/s2i/buildpack) build and optionally push images; quarkus:deploy/k8s:apply workflows; probe wiring from health extension; ConfigMap/Secret integration.
