<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# How do you write a custom class loader in Java

> [!abstract] Short answer
> Extend `ClassLoader`, give the constructor a delegation parent, override `findClass` to produce the bytes, and hand them to `defineClass`. Leave the inherited `loadClass` untouched so parent-first delegation and per-loader caching keep working; register the subclass as parallel capable if several threads will load through it at once.

## What the inherited `loadClass` already does

`loadClass(String)` is `loadClass(String, false)` — locate, do not resolve. The default two-arg implementation runs a fixed order: `findLoadedClass(String)` first, so a loader never defines the same binary name twice; then `loadClass` on the parent loader, with a `null` parent falling to the class loader built into the virtual machine; only then `findClass(String)`. If the class was found and the `resolve` flag is true, it calls `resolveClass`. The javadoc is explicit about the override point: subclasses are encouraged to override `findClass(String)`, rather than `loadClass`; unless overridden, `loadClass` synchronizes on the `getClassLoadingLock` object for the whole load.

## Override `findClass`, then define

`findClass` is the intended hook: it is invoked by `loadClass` after the parent has been checked, and the default implementation throws `ClassNotFoundException`. Inside your override you fetch the bytes from whatever source you own and call `defineClass`, which converts an array of bytes into an instance of class `Class` — but does not initialize it. The binary name you pass must match the name inside the class file, with nested classes using `$` (`com.app.Outer$Inner`).

```java
public class NetworkClassLoader extends ClassLoader {
    private final Path root;

    public NetworkClassLoader(ClassLoader parent, Path root) {
        super(parent);                       // e.g. ClassLoader.getSystemClassLoader()
        this.root = root;
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] bytes = loadClassData(name);  // your source of bytes
        if (bytes == null) {
            throw new ClassNotFoundException(name);
        }
        return defineClass(name, bytes, 0, bytes.length);
    }

    private byte[] loadClassData(String name) {
        Path file = root.resolve(name.replace('.', '/') + ".class");
        try {
            return Files.readAllBytes(file);
        } catch (IOException e) {
            return null;                     // not found here -> parent chain already tried
        }
    }
}
```

**Listing 1.** The shape mirrors the documented template: `loadClass` delegates and caches, `findClass` supplies the bytes, `defineClass` turns them into a `Class`.

Sources for the bytes are arbitrary: a class could be downloaded across a network, generated on the fly, or extracted from an encrypted file — that is the stated reason user-defined loaders exist. What you get is isolation: classes defined by your loader live apart from the same names defined elsewhere ([[What happens if two class loaders load the same class]], [[How would you explain Java class loaders and dynamic class loading]]).

```d2
direction: right
req: "loadClass(name)" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
cache: "findLoadedClass" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
parent: "parent.loadClass" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
mine: "findClass(name)" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
def: "defineClass" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
miss: "ClassNotFoundException" {
  width: 190
  height: 50
  style.fill: "#ffebee"
}
req -> cache
cache -> parent: miss
parent -> mine: miss
mine -> def: bytes
mine -> miss
```

**Fig. 1.** Your code owns only the orange step; the delegation walk and the per-loader cache come from `ClassLoader` itself.

## Parallel capable, or one big lock

A non-parallel-capable loader holds one monitor for every `loadClass`, so two threads loading unrelated classes still serialize — and loaders with non-hierarchical delegation can deadlock on that lock. Class loaders that support concurrent loading register themselves at class-initialization time by invoking `ClassLoader.registerAsParallelCapable()`; the base `ClassLoader` class is registered as parallel capable by default, but a subclass still needs to register itself to inherit that behavior. `getClassLoadingLock` then hands out per-name lock objects instead of locking the whole loader.

> [!warning] Override `loadClass` only to change the walk, never for bytes
> If you override `loadClass` and skip the `findLoadedClass` or parent steps, you lose the guarantees those steps carry: per-loader uniqueness and parent-first visibility ([[How would you explain Classloader parent delegation model]]). Overriding `findClass` keeps the documented algorithm intact — that is why the javadoc prefers it.

> [!warning] A defined class is not an initialized class
> `defineClass` only creates the `Class` object. No `<clinit>` runs at this point; it runs at the first active use, and `resolveClass` or the `resolve` flag link the class but still do not initialize it ([[What triggers class initialization in Java]]).

> [!tip] Interview answer
> **Subclass `ClassLoader`, pass the parent, override `findClass`, and call `defineClass` with your bytes. The inherited `loadClass` already handles caching, parent-first delegation and locking — you only supply the bytes and, for concurrent use, call `registerAsParallelCapable()`. Define once per name, initialize lazily on first active use.**

