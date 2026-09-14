<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What is the application class loader in Java and what does it load

> [!abstract] Short answer
> **The application class loader — officially the system class loader — is the built-in loader that defines classes from the application class path, module path and JDK tools; its built-in name is app.** You reach it with ClassLoader.getSystemClassLoader(). It is the default delegation parent for new ClassLoader instances and is typically the loader used to start the application. The platform loader is its parent or ancestor, so it sees platform classes by delegating upward ([[How would you explain the Java class loader]]).

## Identity and position

The ClassLoader documentation introduces it twice under two names: the system class loader, "also known as application class loader", distinct from the platform class loader. One object, two labels — interviews use application class loader, the accessor and property names say system (getSystemClassLoader, java.system.class.loader). Its built-in name is app, which is the cleanest way to tell it apart from the platform loader in loader traces ([[What is the platform class loader in Java and what does it load]]).

It is created early: the method is first invoked early in the runtime's startup sequence, at which point it creates the system class loader. Its parent or ancestor is the platform loader, so the system class loader can load platform classes by delegating up the chain ([[How would you explain Classloader parent delegation model]]).

## What it defines

The system class loader is typically used to define classes on the application class path, the module path, and JDK-specific tools. The system property java.class.path is read during early initialization of the VM to determine the class path. If the initial module is named, the built-in system class loader has no class path and searches for classes and resources using the application module path; if the initial module is unnamed, an empty java.class.path means the class path is set to the current working directory. JAR files on the class path may carry a Class-Path manifest attribute listing dependent JARs, and invalid Class-Path entries are ignored ([[What is the Java classpath]]).

```d2
direction: down
main: "main class on\nclass path or module path" {
  width: 250
  height: 55
  style.fill: "#e3f2fd"
}
app: "application loader\nname app" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
plat: "platform loader\nSE APIs + implementations" {
  width: 280
  height: 55
}
boot: "bootstrap\ncore modules" {
  width: 180
  height: 50
}
main -> app: "defined here"
app -> plat: "delegate up"
plat -> boot: "delegate up"
```

**Fig. 1.** Your classes are defined at the bottom of the built-in chain; everything platform-shaped is reached by delegating upward.

## The default parent for user loaders

The accessor documentation states the second role plainly: the system class loader is the default delegation parent for new ClassLoader instances. Construct a ClassLoader subclass without naming a parent and application classes flow through your loader by delegation. The same method is also typically the class loader used to start the application, which is why throwing the system loader away is not an option and plugin isolation is done with child loaders instead ([[What happens if two class loaders load the same class]]).

```java
class AppLoaderFacts {
    static class PluginLoader extends ClassLoader {
        PluginLoader() {
            super();  // default parent: getSystemClassLoader()
        }
    }

    public static void main(String[] args) {
        ClassLoader app = ClassLoader.getSystemClassLoader();
        System.out.println(app.getName());                        // app
        System.out.println(app.getParent().getName());            // platform
        System.out.println(new PluginLoader().getParent() == app); // true
    }
}
```

**Listing 1.** The name, the parent chain and the default-parent contract for user loaders, all observable in three lines.

> [!warning] Two easy traps
> The word system has nothing to do with the platform or bootstrap loaders — it is the application loader's other name, and "system classes" are not what it defines. And during startup the return value of getSystemClassLoader() should not be cached before the system is fully initialized: the method runs early in the startup sequence, and code that runs this early is executing in a runtime that is still warming up ([[What happens in the JVM when a Java application starts]]).

> [!tip] Interview answer
> **The application class loader, formally the system class loader, is the built-in loader named app that defines classes from the application class path, module path and JDK tools.** Created early in startup, parent or ancestor chain runs through the platform loader to bootstrap. It is the default delegation parent of new ClassLoader instances, so your custom loaders inherit application and platform visibility unless you choose a different parent.
