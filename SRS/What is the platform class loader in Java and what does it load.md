<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What is the platform class loader in Java and what does it load?

> [!abstract] Short answer
> **The platform class loader is the middle built-in loader, public API since Java 9: it loads the platform classes — the Java SE platform APIs, their implementation classes and JDK-specific run-time classes.** Reach it with ClassLoader.getPlatformClassLoader(); its built-in name is platform. It sits between the bootstrap loader (its parent) and the system loader (which has it as parent or ancestor), and it is the recommended parent for user loaders that must see platform classes but not application classes.

## Responsibility

The ClassLoader documentation lists three built-in loaders, and the platform one is responsible for loading the platform classes: the Java SE platform APIs, their implementation classes, and JDK-specific run-time classes defined by the platform class loader or its ancestors. All platform classes are visible to it ([[What is the Java Platform Module System]]).

The loader can also serve as the parent of a ClassLoader instance — that is its intended role for user-defined loaders that should see platform classes but stay isolated from the application. The constructor API note spells out the alternative: if the parent is specified as null (for the bootstrap class loader) then there is no guarantee that all platform classes are visible, so a loader that needs the whole SE API should be parented on getPlatformClassLoader() ([[How do you write a custom class loader in Java]]).

```d2
direction: right
boot: "bootstrap\nnull - core modules" {
  width: 230
  height: 55
}
plat: "platform\nSE APIs + implementations" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
app: "application\nclass path + module path" {
  width: 270
  height: 55
}
user: "your loader\nparented on platform" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
plat -> boot: "parent"
app -> plat: "parent or ancestor"
user -> plat: "parent"
```

**Fig. 1.** The platform loader sits in the middle of the built-in chain and doubles as the documented parent for loaders that must see platform classes while staying isolated from the application.

## Where it came from

Java 9 replaced the old extension loader with the platform loader: in its new role the loader is known as the platform class loader, it is available via the ClassLoader.getPlatformClassLoader method, and it is required by the Java SE Platform API Specification. The reorganization doubled as a security cleanup — types loaded by the bootstrap loader are implicitly granted all security permissions, so modules that do not actually require all permissions were de-privileged and moved to the platform loader ([[What is the difference between the extension and platform class loaders]]). Its built-in name is platform, and it is the parent or an ancestor of the system loader ([[What is the application class loader in Java and what does it load]]).

```java
class PlatformLoaderFacts {
    public static void main(String[] args) {
        ClassLoader platform = ClassLoader.getPlatformClassLoader();

        System.out.println(platform.getName());            // platform
        System.out.println(platform.getParent());          // null: bootstrap
        System.out.println(platform.getParent() == null);  // true
    }
}
```

**Listing 1.** The accessor, the built-in name and the bootstrap parent. Every built-in chain walks through this loader on its way up, which is why platform classes resolve from custom loaders too.

> [!warning] Parent-first is the default, not a law
> To allow upgrading and overriding of modules defined to the platform class loader, the loader may have to delegate to other class loaders — the application class loader, for example. In other words, classes in named modules defined to loaders outside the platform chain may still be visible to the platform loader. Parent-first delegation is a default policy, and the platform loader is the documented exception ([[How would you explain Classloader parent delegation model]]).

> [!tip] Interview answer
> **The platform class loader loads the platform classes: Java SE APIs, their implementations and JDK run-time types, defined by it or its ancestors.** Public since Java 9 via getPlatformClassLoader(), built-in name platform, parent is the bootstrap loader, and it is the parent or ancestor of the system loader. It replaced the extension loader, partly to de-privilege modules that do not need the bootstrap loader's all-permissions grant.
