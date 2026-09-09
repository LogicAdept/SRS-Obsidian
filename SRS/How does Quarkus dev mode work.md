<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: ./mvnw quarkus:dev (or Gradle equivalent) starts development mode: the app boots fast, "Profile dev activated. Live Coding activated.".
Live reload: changed Java files are recompiled in the background and the running app is redeployed on refresh; worker threads keep state where possible.
Also in dev mode: Dev Services start automatically; Dev UI at /q/dev; continuous testing can run changed tests in the background; pom.xml changes restart the Maven process.
Debugging on port 5005 by default (suspend optional); HTTP usually on 8080.
Trap: some changes (build-time config, new extensions, bean scope changes) require a full restart, not just live reload.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
