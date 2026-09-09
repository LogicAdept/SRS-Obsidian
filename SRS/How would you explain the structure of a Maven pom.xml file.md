<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How would you explain the structure of a Maven pom.xml file

> [!abstract] Short answer
> **The POM is the project's single declarative model: coordinates that identify it, properties, dependencies it consumes, and build/plugin configuration for how it is built and packaged.** `modelVersion` pins the POM schema; `groupId:artifactId:version` is the artifact's address; everything else — layout, lifecycle wiring — is inherited convention you override only when needed.

## The skeleton, minimal but real

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.demo</groupId>
    <artifactId>demo-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
        </plugins>
    </build>
</project>
```

**Listing 1.** A working POM (it built successfully with Maven 3.9.9 on JDK 21). Coordinates, one test dependency with a scope, one pinned plugin.

The block map: coordinates (`groupId`, `artifactId`, `version`, `packaging`) make the artifact resolvable in repositories; `properties` are named values referenced as `${...}` and used to pin compiler release and encoding; `dependencies` declares what the classpath needs — resolution rules and scopes in [[What are the dependency scopes in a Maven pom]]; `build/plugins` configures the goals that execute phases — the phase model in [[How would you explain the Maven build lifecycle]]. Two more blocks matter at scale: `dependencyManagement` centralizes versions so child modules inherit them without restating, and `parent`/`modules` tie a reactor of modules into one versioned build.

```d2
direction: right
id: "Coordinates\nG:A:V + packaging" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
props: "Properties\nrelease, encoding, ${vars}" {
  width: 270
  height: 90
  style.fill: "#e3f2fd"
}
deps: "Dependencies\nwhat the classpath needs" {
  width: 270
  height: 90
  style.fill: "#fff3e0"
}
build: "Build plugins\nhow phases execute" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
mgmt: "At scale: dependencyManagement\nparent + modules" {
  width: 330
  height: 90
  style.fill: "#e8f5e9"
}
id -> mgmt
props -> mgmt
deps -> mgmt
build -> mgmt
```

**Fig. 1.** The POM's four everyday blocks, with the version-management machinery that kicks in for multi-module builds.

> [!warning] The POM you write is not the POM Maven builds with
> The `effective-pom` is the merge of your POM with its parents and the Super POM — the built-in defaults every project silently inherits (plugin versions, resource handling, directory layout). Interview trap: claiming "the POM has no jar plugin, so nothing packages it" — the default bindings come from the lifecycle, not from your file. Check reality with `mvn help:effective-pom` and resolve versions the same way. Also: `version` and scope omissions are never "nothing" — an omitted scope is `compile`, an omitted version (outside management) fails or drifts, and `packaging` defaults to `jar`. What lands on the classpath from those dependencies is decided by [[What are the dependency scopes in a Maven pom]], and the command that packages it all is [[How would you explain mvn clean install]].

> [!tip] Interview answer
> **A pom.xml is the declarative project model. Top: modelVersion and the coordinates groupId, artifactId, version plus packaging. Then properties, dependencies with scopes, and the build section with plugins bound to lifecycle phases. For multi-module builds, parent and modules tie versions together and dependencyManagement centralizes them. Maven merges your file with inherited defaults into the effective POM, so the file only overrides what needs overriding.**

