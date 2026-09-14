<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What is the difference between the maven-shade-plugin and the maven-assembly-plugin

> [!abstract] Short answer
> **Shade builds an uber-JAR: it merges your classes and dependency classes into one JAR and replaces the project's main artifact, with package relocation to defuse classpath conflicts. Assembly builds distribution archives — zip, tar.gz, directories — from a descriptor, and can include much more than dependencies; it does not have to produce a JAR at all.**

Both are "get my project plus its dependencies into a deployable shape" tools, but they answer different questions. Shade answers "one runnable JAR": the `shade:shade` goal, bound to the `package` phase ([[What are the phases of the three Maven lifecycles]] places it among the bindings), takes the original jar, unpacks dependency jars into it, applies resource transformers, and installs the result **as the project artifact** — downstream modules and `install:install` see the shaded jar, not the thin one. Assembly answers "a distributable bundle": `assembly:single` reads an assembly descriptor and lays out archives containing binaries, dependency jars, scripts, docs — whichever file-sets the descriptor names.

## Where each one hurts

```d2
direction: down
shade: "maven-shade-plugin\npackage phase → uber-JAR\nreplaces main artifact" {
  width: 320
  height: 110
  style.fill: "#e3f2fd"
}
reloc: "Relocation renames packages\ncom.google → shaded.com.google" {
  width: 340
  height: 100
  style.fill: "#e3f2fd"
}
trans: "Resource transformers merge clashes\nMETA-INF/services, manifests" {
  width: 350
  height: 100
  style.fill: "#e3f2fd"
}
asm: "maven-assembly-plugin\ndescriptor → zip / tar.gz / dir" {
  width: 330
  height: 110
  style.fill: "#e8f5e9"
}
formats: "Prefabricated descriptors:\nbin · jar-with-dependencies\nproject · src" {
  width: 340
  height: 110
  style.fill: "#e8f5e9"
}
shade -> reloc -> trans
asm -> formats
```

**Fig. 1.** Shade's problem domain is class-level collisions inside one JAR; assembly's is packaging arbitrary content into distributable formats.

The assembly plugin's `jar-with-dependencies` descriptor is the naive uber-JAR: it unpacks dependency jars alongside your classes without relocation or transformers. Two dependency versions of the same library overwrite each other's classes silently, and `META-INF/services` entries get lost — shade exists precisely because of that, with relocation renaming moved packages and rewriting bytecode references, and transformers like `ServicesResourceTransformer` merging service descriptors instead of dropping them ([[What does the maven-dependency-plugin do]]'s `copy-dependencies` is the third, even simpler route: keep separate jars, ship a folder).

> [!warning] Shading replaces the artifact, not just adds a file
> After shading, `target/` still contains the original thin jar (kept as `original-...jar`), but the artifact installed and deployed by `install`/`deploy` is the shaded one. Teams that expected the plain jar downstream — say, as a library dependency — get a shadowed dependency tree instead. If you need both shapes, that is a job for the assembly plugin or a classifier-attached extra artifact, not shade.

> [!tip] Interview answer
> **Shade makes an uber-JAR and swaps it in as the project artifact — it handles dependency collisions with package relocation and resource transformers, so libraries keep working inside one jar. Assembly assembles distribution bundles (zip, tar, folders) from a descriptor with file-sets and permissions; its jar-with-dependencies shortcut merges jars naively and can lose service files. One-jar deployable: shade. Installable bundle with scripts and configs: assembly.**
