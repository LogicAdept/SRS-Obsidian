<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# What are the bootstrapping phases of a Quarkus application

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Quarkus boot is split into phases — augmentation (build time), static init (recorded bootstrap replay at startup), and runtime execution.
A Quarkus application main is a generated CLASS_INIT runner; work is classified as build-time init (done by extensions during augmentation), STATIC_INIT (runs once at application start), or RUNTIME_INIT.
The start order and what runs in each phase is the interview point: why some config and beans must be build-time, why static init must avoid dynamic features.
