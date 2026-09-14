<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What is the bootstrap class loader in the JVM and what does it load?

> [!abstract] Short answer
> **The bootstrap class loader is the one loader the virtual machine itself supplies: it has no parent, it is typically represented as null, and every delegation chain ends there.** The spec recognizes exactly two kinds of loaders — the bootstrap loader supplied by the JVM and user-defined loaders that subclass ClassLoader ([[How would you explain the Java class loader]]). It loads the core Java SE and JDK modules by locating their binaries in a platform-dependent manner and asking the VM to derive the run-time Class. In the API you never hold it — null stands in for it.

## What the spec fixes

The JVM specification names two kinds of class loaders: the bootstrap class loader supplied by the Java Virtual Machine, and user-defined class loaders. Every user-defined loader is an instance of a subclass of the abstract ClassLoader; the bootstrap loader is not something you construct, subclass, or get a reference to. The Class API shows it only as an absence: types the bootstrap loader defined answer null to getClassLoader(), and the built-in loader chain terminates at it ([[How would you explain Classloader parent delegation model]]).

Its job is to locate the binaries of the core platform classes. When a user-defined chain cannot find a name and delegation runs out of parents, the VM passes the request to the bootstrap loader. It finds a purported representation of the class in a platform-dependent manner and asks the VM to derive the run-time class from it. If no representation is found, it throws ClassNotFoundException, and the load that triggered the delegation fails with NoClassDefFoundError ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

```d2
direction: down
request: "load name N" {
  width: 170
  height: 40
}
app: "application loader" {
  width: 220
  height: 45
}
plat: "platform loader" {
  width: 200
  height: 45
}
boot: "bootstrap loader\nno parent - null in the API" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
vm: "VM derives the Class\nin the method area" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
request -> app: "parent-first"
app -> plat
plat -> boot: "delegation terminus"
boot -> vm: "locate binary, ask VM to derive"
```

**Fig. 1.** Parent-first delegation ends at the bootstrap loader; it is the only loader the VM itself supplies, and its parent slot is empty by definition.

## What it loads

The bootstrap loader defines the core Java SE and JDK modules. Since Java 9 it is implemented in both library code and within the virtual machine, but for compatibility it is still represented by null in the ClassLoader API. Historically it was also where all platform classes lived; today selected Java SE and JDK modules are defined by the platform loader instead ([[What is the platform class loader in Java and what does it load]]).

```java
class WhoDefinesWhat {
    public static void main(String[] args) {
        // core platform class: bootstrap-defined, so the answer is null
        System.out.println(String.class.getClassLoader());            // null

        // the platform loader's own parent is the bootstrap loader
        System.out.println(ClassLoader.getPlatformClassLoader()
                .getParent());                                        // null

        // two parents up from the application loader is the same boundary
        System.out.println(ClassLoader.getSystemClassLoader()
                .getParent().getParent());                            // null
    }
}
```

**Listing 1.** Bootstrap-defined types surface as null in every probe: on the classes themselves and on the parent chain of the built-in loaders.

> [!warning] The primordial nickname is folklore
> Older literature calls this loader the primordial class loader. Neither the JVM specification nor the ClassLoader javadoc uses that name; both say bootstrap class loader. An interview answer that says primordial will be understood, but the spec term is the safe one to commit to.

> [!warning] Not every platform class is bootstrap-defined
> A null answer from getClassLoader() does not generalize across the JDK: since Java 9 the platform loader defines selected Java SE and JDK modules, so some platform types report the platform loader rather than null. Core types such as String stay bootstrap-defined. Bootstrap-defined types are also implicitly granted all security permissions, which is exactly why the split exists — modules that do not need every permission were moved out from behind that boundary. Note also that a custom loader parented on null gets no guarantee that all platform classes are visible, because null means bootstrap, and only ancestors of the platform loader see all platform classes.

> [!tip] Interview answer
> **The bootstrap class loader is the VM-supplied loader: no parent, typically represented as null, terminus of every delegation chain.** It loads the core Java SE and JDK modules, locating binaries in a platform-dependent way and asking the VM to derive the Class. It is not a ClassLoader object you can reference — you see it only as null — and the old primordial name is literature folklore, not spec wording.
