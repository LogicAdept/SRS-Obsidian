<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Build #SRS

# What is an executable JAR in Spring Boot?

> [!abstract] Short answer
> A Boot **executable JAR** is a **nested-jar archive** produced by the Maven/Gradle plugin’s **`repackage`** goal: your classes in **`BOOT-INF/classes`**, dependencies as real jars in **`BOOT-INF/lib`**, loader classes at the root. **`Main-Class`** is **`JarLauncher`**; **`Start-Class`** is your `main`. Run it with **`java -jar`**. Java cannot load nested jars by itself — this is **not** a shaded uber-jar and **not** a plain `maven-jar-plugin` artifact.

## Nested jars, not a shade

Java has **no** standard way to load a jar inside a jar. Shade/uber tools flatten every class into one tree (duplicate filenames clash; you cannot see which library you shipped). Boot **nests** the original jars and uses **`org.springframework.boot.loader.launch.JarLauncher`** as the bootstrap `Main-Class`. That launcher builds a `ClassLoader` over `BOOT-INF/lib/` and then calls your **`Start-Class`**.

```
example.jar
 +- META-INF/MANIFEST.MF
 +- org/springframework/boot/loader/…
 +- BOOT-INF/classes/…          # application
 +- BOOT-INF/lib/dependency.jar # nested jars
```

**Listing 1.** Loader-compatible layout. `classpath.idx` orders those nested jars for `java -jar` (not for IDE / `spring-boot:run`). `layers.idx` is for Docker/OCI layers.

```
Main-Class: org.springframework.boot.loader.launch.JarLauncher
Start-Class: com.mycompany.project.MyApplication
```

**Listing 2.** Manifest the plugin writes. Do **not** put `Main-Class` on `maven-jar-plugin` — configure **`spring-boot-maven-plugin`**. No `Class-Path` entries; the nested jars **are** the classpath.

```xml
<plugin>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-maven-plugin</artifactId>
</plugin>
```

**Listing 3.** With **`spring-boot-starter-parent`**, this already binds **`repackage`**. Otherwise add an execution of goal **`repackage`** (it rewrites the jar from the `package` phase: `mvn package spring-boot:repackage`). Gradle: `bootJar`.

```bash
java -jar myapp.jar
```

**Listing 4.** That is the documented start command. A **web** app also contains an **embedded** server in `BOOT-INF/lib` — no separate Tomcat install ([[Which embedded containers are supported by Spring Boot]]). A **non-web** executable JAR is the same layout **without** a server ([[How do you create a non-web Spring Boot application]]).

```d2
direction: right
thin: "maven-jar-plugin\nthin jar" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
repkg: "repackage\nBOOT-INF + JarLauncher" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
run: "java -jar\nStart-Class main()" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}

thin -> repkg -> run
```

**Fig. 1.** Executable **WAR** is the sibling layout (`WarLauncher`, `WEB-INF/lib` + `lib-provided`) ([[How do you deploy a Spring Boot application as a WAR]]; [[How do you deploy a Spring Boot application]]).

> [!warning] A plain Maven JAR is not this
> `maven-jar-plugin` alone does **not** nest `BOOT-INF/lib` or install `JarLauncher`. `java -jar` on that artifact fails unless you already have every dependency on the classpath. **`layout=NONE`** also skips the loader. If another module depends on this project, keep a **classifier** on the repackaged jar — classes live under **`BOOT-INF/classes`** and are invisible as a normal library.

> [!warning] “Fully executable” is a different file
> `<executable>true</executable>` / Gradle `launchScript()` prepends a Unix script so you can `./myapp.jar` as init.d. Some tools (`jar -xf`) then **fail**. Use that only when you will exec the file **directly**; **`java -jar` does not need it**. Zip64 outer jars cannot be fully executable. Do not confuse this with shade: Boot still keeps **nested** jars.

> [!tip] Interview answer
> A Spring Boot executable JAR is a nested-jar layout from the repackage goal: my classes in BOOT-INF/classes, dependencies as jars in BOOT-INF/lib, and JarLauncher as Main-Class so java -jar works. Java cannot load nested jars by itself, so a plain Maven jar or a shaded uber-jar is not the same thing. For a web app the nested libs include the embedded server; I do not install Tomcat separately.
