<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How does the Docker build cache work

> [!abstract] Short answer
> The builder checks each instruction against the cache: a layer is reused if the instruction is unchanged (string match for `RUN`, checksum match for `COPY`/`ADD` inputs) and every previous layer was reused. The first miss invalidates **all downstream layers** — even ones whose inputs did not change — so Dockerfile ordering is a performance decision.

## The invalidation cascade

For `RUN apt-get update` the cache keys on the literal command; for `COPY main.c /src/` it keys on the file checksums. One changed `COPY` input forces that layer and everything after it to rerun.

```dockerfile
COPY pom.xml .                        # cached until pom.xml changes
RUN mvn -B dependency:go-offline      # rerun only when the pom layer reruns
COPY src ./src                        # changes on every edit — deliberately LAST
RUN mvn -B package -DskipTests
```

**Listing 1.** Order picked for the cache: the stable dependency layer sits above the volatile source copy, so code edits recompile but never re-download the Maven repository.

```d2
direction: down
l1: "COPY pom.xml\n(cache: checksum)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
l2: "RUN dependency:go-offline\n(cache: command string)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
l3: "COPY src ./src\nchanged -> MISS" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
l4: "RUN mvn package\nrerun despite unchanged inputs" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
l1 -> l2 -> l3 -> l4: "invalidation flows down"
```

**Fig. 1.** A single miss poisons everything below it; the fast path is keeping volatile instructions at the bottom of the Dockerfile.

Config instructions participate too: changing an `ENV` or `WORKDIR` value invalidates all subsequent layers, since later instructions execute in that modified context.

> [!warning] Cache makes late COPYs a correctness trap, not just a speed trap
> The same ordering that speeds builds can hide staleness: `COPY` an old artifact above a changed input and the builder happily reuses it. When a build must not reuse anything, `docker build --no-cache` rebuilds from scratch; for incremental hygiene, structure layers so volatile inputs sit below the outputs that depend on them ([[How would you explain Multi-stage build]] shows the canonical Java split), and keep junk out of the checksum inputs with [[What is a .dockerignore file for]].

> [!tip] Interview answer
> **Each instruction becomes a cached layer; RUN keys on the command string, COPY/ADD on file checksums, and the first miss invalidates every layer after it. So you copy the pom before the sources, dependencies before code, and use --no-cache when you truly need a cold build.**

