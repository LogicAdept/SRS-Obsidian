<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What are Maven build profiles for

> [!abstract] Short answer
> **Profiles are named overrides inside one POM that switch on for specific builds — a different dependency set, plugin configuration, or property value per environment — instead of maintaining several nearly identical POM files.** They activate explicitly (`-P`), by default (`activeByDefault`), or implicitly from the environment (JDK version, OS, properties, file presence).

## Where they live and how they switch on

A profile is a subset of POM elements wrapped in `<profiles>`, defined in three places: per project (`pom.xml`), per user (`~/.m2/settings.xml`), or globally (the settings in the Maven installation). Activation sources: the CLI flag `-P id1,id2` (additive to every other trigger); `<activeByDefault>true</activeByDefault>`, which holds only until any other profile of that POM is activated; and implicit environment triggers — a JDK version match, an OS match, a system or CLI property (`-Denv=dev`), the packaging property, or the presence or absence of a file. Maven 4 additionally refuses to activate or deactivate a profile that does not exist unless its id is marked optional with a `?` prefix.

```xml
<profiles>
    <profile>
        <id>integration-env</id>
        <activation>
            <property>
                <name>env</name>
                <value>it</value>
            </property>
        </activation>
        <properties>
            <it.db.url>jdbc:postgresql://it-db:5432/app</it.db.url>
        </properties>
    </profile>
</profiles>
```

**Listing 1.** An environment-triggered profile: running `mvn verify -Denv=it` injects the integration-test database URL; without the property, the POM's defaults stand.

```d2
direction: right
p1: "-P flag\nexplicit" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
p2: "activeByDefault\nuntil anything else fires" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
p3: "Environment triggers\nJDK, OS, property, file" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
eff: "Effective POM\nfor this build" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
p1 -> eff
p2 -> eff
p3 -> eff
```

**Fig. 1.** All activation sources merge into one effective POM per run — the base POM plus the active profiles' overrides.

Inspect the result rather than guess: `mvn help:active-profiles` lists which profiles fired and where they were declared. A subtle documented rule for senior interviews: profiles are **not inherited** by child POMs — they are resolved early by the model builder, and only the *effects* of active profiles (the plugin or property values they contributed) flow down.

> [!warning] Profiles are how portability leaks out of the build
> The documentation is blunt about the danger: profiles "can easily lead to differing build results from different members of your team" — the build stops being a function of the source tree. The sharpest edge is `activeByDefault`: the moment any profile of that POM is activated by flag or trigger, *all* of that POM's active-by-default profiles switch off — a build silently loses configuration nobody disabled on purpose. Environment-keyed activation (`-Denv=prod`) similarly invites builds that only work where the property happens to be set. And the naming trap: a Maven profile selects build variants at *build* time, while a Spring profile selects bean definitions at *runtime* — they are different tools with the same word on them. Structure the profiles change, not the POM they live in: [[How would you explain the structure of a Maven pom.xml file]]; the phases the overridden plugins bind to: [[How would you explain the Maven build lifecycle]]; the runtime namesake that gets confused with this: [[What is a Spring profile]].

> [!tip] Interview answer
> **Profiles keep one POM but vary it per build: an explicit -P selection, an activeByDefault fallback, or implicit triggers like JDK, OS or a -D property merge overrides into the effective POM. I use them sparingly — for genuinely environment-bound bits — because they make builds differ between machines, and activeByDefault vanishes the moment anything else activates. And no, a Maven profile is not a Spring profile: one picks build inputs, the other picks runtime beans.**

