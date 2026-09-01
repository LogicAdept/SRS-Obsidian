<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS

# What is reflection in Java?

> [!abstract] Short answer
> **Programmatic access to the fields, methods, and constructors of classes that are already loaded, and then using those reflected members on the live objects — still inside encapsulation and security rules.** `java.lang.Class` plus `java.lang.reflect` are that API. You inspect a runtime type you did not hard-code, then construct, invoke, or read/write. Since 1.1.

## Inspect loaded types, then operate

The package “provides classes and interfaces for obtaining reflective information about classes and objects.” Reflection is not a second compiler and not a way to invent a type that the VM has not loaded. You obtain a `Class` ([[What is the Class class in Java reflection]], [[How can you get the Class object in Java]]), ask it for `Field` / `Method` / `Constructor` (public-and-inherited vs declared-here), and then `get` / `set` / `invoke` / `newInstance` ([[How can you invoke a method using reflection]], [[How can you create an instance of a class using reflection]]).

```d2
direction: down
c: "Class (loaded type)" {
  width: 220
  height: 45
}
look: "getMethod / getField /\ngetConstructor (or declared)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
run: "invoke / get-set / newInstance" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
c -> look
look -> run
```

**Fig. 1.** Two jobs: describe a loaded type, then use a member. The platform names debuggers, class browsers, Object Serialization, and JavaBeans as the kinds of program that need this ([[What are some use cases of Java reflection]]).

`AccessibleObject.setAccessible` can suppress language access checks when permission allows; modules can still refuse ([[What does setAccessible do in the Reflection API]]). `Array` and `Proxy` are the same idea for arrays and interface-based stand-ins ([[What is a dynamic proxy in Java reflection]]).

Core reflection presents a **JVM** model (`class` file, synthetic members, bridges, class loaders), not a one-to-one picture of Java source. A compiler may add methods you never wrote; modifiers on the `Class` need not match the source declaration.

```java
class Idea {
    static Object call(Object target, String method) throws Exception {
        Method m = target.getClass().getMethod(method);
        return m.invoke(target);
    }
}
```

**Listing 1.** The type and the member arrive at runtime as objects and strings. The compiler does not check that `method` exists; `NoSuchMethodException` does.

The Oracle Reflection trail treats this as an advanced tool: if the same operation can be a normal call, prefer that. Reflective dispatch is slower, names are not type-checked, and reaching `private` state couples you to layout that can change ([[What are the drawbacks of using Java reflection]]).

> [!warning] Loaded, not “any name you type”
> `forName` still has to locate a class the loader can define. Reflection does not compile source on the fly. A missing binary name is `ClassNotFoundException`, not a new type.

> [!warning] Not a replacement for a typed call
> Everyday code that already imports `Foo` should call `Foo`. Reflection is for types and members that are not fixed at the call site.

> [!tip] Interview answer
> **Reflection is runtime metadata plus use: get a `Class`, look up members, then invoke or read them — including types the calling code did not name.** It is `java.lang.Class` and `java.lang.reflect`, on **loaded** classes, still subject to access control. **If you already know the type, a normal method call is the design; this API is for tools, serializers, plugins, and proxies.**
