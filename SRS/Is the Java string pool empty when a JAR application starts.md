<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory/Heap #SRS

# Is the Java string pool empty when a JAR application starts?

> [!abstract] Short answer
> **No.** By the time your `main()` runs, the JVM has loaded, linked, and initialized a large part of the core library, and literals of those classes are interned as they resolve ([[How do string literals enter the Java string pool]]). On a stock JDK 21 hello-world, `-XX:+PrintStringTableStatistics` reports on the order of **~2 700 entries** — all without a single line of your code interning anything. The `intern()` javadoc's "a pool of strings, initially empty" describes the JVM's zero point, not the state at application start — [[What is the Java string pool]], [[What happens in the JVM when a Java application starts]].

## What populates it before main

- **Bootstrap loading** — `String`, `System`, `Integer`, charsets, collections, and the launcher machinery are loaded and initialized before your class; each resolved literal ("java", "main", format strings, exception messages' fragments) lands in the table.
- **Lazy, per use** — resolution canonicalizes a literal the first time the instruction using it runs ([[How do string literals enter the Java string pool]]), so the table grows with *executed* core code paths, not with every class file on the module path.
- **Your classes** — literals of your `main` class join only when reached, which is why the count keeps creeping up during a slow warm-up.

```bash
java -XX:+PrintStringTableStatistics -jar app.jar   # statistics at JVM exit
# StringTable statistics:
#   Number of buckets       : 65536
#   Number of entries       : 2697      <- hello-world, JDK 21
jcmd <pid> VM.stringtable                            # same view, live process
```

**Listing 1.** Reproduce it yourself: run any trivial app with `PrintStringTableStatistics` and read the entry count at exit; attach `jcmd VM.stringtable` seconds after start and it is already in the thousands on a real application. Verified on JDK 21.

```d2
direction: down
zero: "JVM zero point\npool 'initially empty' (intern() javadoc)" {
  width: 340
  height: 66
  style.fill: "#fff8e1"
}
boot: "Bootstrap classes load + resolve literals\nString, System, collections, charsets…" {
  width: 380
  height: 66
  style.fill: "#e3f2fd"
}
main: "main() starts\npool already holds thousands of entries" {
  width: 380
  height: 60
  style.fill: "#e8f5e9"
}
zero -> boot -> main
```

**Fig. 1.** Application start is not the pool's start: the bootstrap phase fills the table before your first statement.

> [!warning] "Empty at start" and "all literals at load" are both myths
> The pool is neither empty when `main` begins, nor preloaded with every literal your JAR contains — resolution is lazy, so a big fat JAR does not mean a big table at startup. And the pre-sized bucket count (`-XX:StringTableSize`, default 65536 on JDK 21) is capacity planning for the hash table, not the number of strings in it.

> [!tip] Interview answer
> No — and I can prove it: `-XX:+PrintStringTableStatistics` on a hello-world shows thousands of entries on JDK 21. The launcher and core bootstrap classes resolve their literals before `main()` runs, and each resolution interns into the table. It is still lazy though: your own classes contribute only the literals they actually execute, so at startup the table is populated by the platform, not by your JAR.
