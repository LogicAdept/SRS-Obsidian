<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How do you bind a plugin goal to a lifecycle phase in Maven

> [!abstract] Short answer
> **Declare the plugin in `<build><plugins>` and add an `<execution>` naming the `<phase>` and the `<goals>`; the execution's `<configuration>` merges with the plugin-level one.** Goals can also carry a default phase from their `@Mojo` annotation, packaging supplies the built-in bindings, and `<pluginManagement>` centralizes versions and default configuration for the whole inheritance tree.

An execution is the unit of binding: it pairs goals with a phase and its own configuration. The execution's `id` is what makes reuse sane — Maven's built-in bindings have recognizable ids like `default-compile`, and during POM inheritance or profile application an execution with a matching id merges its configuration into the inherited one, while a new id adds an extra execution. Multiple `<execution>` blocks run the same goal with different configurations; what is forbidden is declaring the same plugin twice in `<plugins>` — Maven 3 warns, Maven 4 fails the build.

## Anatomy and the management layer

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.mycompany.example</groupId>
      <artifactId>display-maven-plugin</artifactId>
      <version>1.0</version>
      <executions>
        <execution>
          <id>show-test-start</id>
          <phase>process-test-resources</phase>
          <goals>
            <goal>time</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
  <pluginManagement>
    <plugins>
      <plugin>
        <groupId>com.mycompany.example</groupId>
        <artifactId>display-maven-plugin</artifactId>
        <version>1.0</version>
        <configuration>
          <format>iso</format>
        </configuration>
      </plugin>
    </plugins>
  </pluginManagement>
</build>
```

**Listing 1.** An explicit binding to `process-test-resources`; `<pluginManagement>` would pin the version and default `<configuration>` for every module that declares the plugin without a version.

Configuration accumulates from four places: the plugin descriptor's defaults, `<pluginManagement>`, the plugin-level `<configuration>`, and the execution's `<configuration>` — more specific levels override matching elements and add new ones, and `combine.children`/`combine.self` attributes fine-tune how inherited lists merge. Ordering within a phase is defined: packaging-bound goals run first, then POM-declared ones in declaration order. A plugin (or a single execution) can opt out of inheritance with `<inherited>false</inherited>` — the standard answer to "how do I stop this plugin propagating to child POMs" in a multi-module reactor ([[How do multi-module Maven builds work]]); conversely, profiles can add or reconfigure executions per environment ([[What are Maven build profiles for]]). If the plugin's goal already declares a sensible `defaultPhase` ([[How do you write a custom Maven plugin]]), an `<execution>` with only `<goals>` is enough — the phase is implicit.

> [!warning] Declaring a version twice is how drift starts
> The parent usually manages the plugin version, so a child that hard-codes its own version silently builds with two different plugin versions in one reactor. Either rely on `<pluginManagement>` and omit the version, or consciously override it — never copy the version block "just to be explicit".

> [!tip] Interview answer
> **Bindings live in `<executions>`: each execution names goals, a phase (or relies on the goal's default), an id, and optionally its own configuration. Ids matter because inherited executions with the same id merge configurations while new ids add runs; pluginManagement in the parent pins versions and defaults; inherited=false keeps a plugin local to the declaring POM. Packaging bindings always run first, then POM ones in declaration order.**
