<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP #SRS

# How would you explain static typing in Java?

> [!abstract] Short answer
> Java is **statically typed**: every **variable** and every **expression** has a **compile-time type**. It is also **strongly typed**: that type limits which values you may store and which operations you may apply, so many mistakes are **compile-time errors**. A reference variable’s type may be a **superclass or interface**; the object still has a **run-time class** ([[How would you explain main concepts OOP class object interface]]). That gap is subtype polymorphism, not a lack of static types ([[What is polymorphism]]). Variables: [[How would you explain kinds of variables in Java such as local and instance]].

## Compile-time type vs class of the object

The compiler assigns a type to `x` in `Shape x = new Circle();` (`Shape`) and to the expression `new Circle()` (`Circle`). Assignment is allowed only when the value is **assignment-compatible** with the variable. Primitive variables hold exactly that primitive type. Reference variables hold `null` or a reference to an instance of the type or a subtype (an interface-typed variable refers to a **class** instance that implements it).

**What is still checked at run time.** Casts, array stores (`String[]` aliased as `Object[]`), and generic **heap pollution** after unchecked operations. Type arguments are **not reified**: `List<String>` and `List<Integer>` share one class at run time. Overload resolution uses compile-time types; overriding uses the run-time class ([[How would you explain Overload vs Override]]; [[How would you explain dynamic runtime polymorphism in Java]]).

`var` does not make Java dynamically typed: the local’s type is **inferred** at compile time and then fixed. Reflection and `invokevirtual` still see JVM classes; that does not erase the compile-time checks on source.

```d2
direction: down
ct: "compile-time type\nShape x" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
rt: "run-time class\nCircle" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
ct -> rt: "x refers to"
```

**Fig. 1.** Static typing names the variable. The object still has a class. Both exist at once.

```java
class Use {
    static void go() {
        String s = "hi";
        Object o = s;
        String t = (String) o;
        o = Integer.valueOf(1);
    }
}
```

**Listing 1.** `o = s` is legal: `String` is a subtype of `Object`. `int n = s` would not compile. `(String) o` is a run-time check; after `o` holds an `Integer`, that cast would throw `ClassCastException`.

> [!warning] Static typing is not “no polymorphism”
> `Shape x = new Circle(); x.area();` is statically typed **and** dispatched on the run-time class. The compiler proves `area` exists on `Shape`. It does not pick `Circle.area` until run time. Overloading is the compile-time half of “which method.”

> [!warning] `var`, generics, and `Object` are still static
> `var x = "hi"` has compile-time type `String`. `List<String>` is checked at compile time; at run time the list is a raw `List`. Putting an `Integer` in through an unchecked warning is heap pollution, not dynamic typing.

> [!warning] Arrays are covariant and checked on store
> `Object[] a = new String[1]; a[0] = Integer.valueOf(1);` compiles and then throws `ArrayStoreException`. Most other assignments are rejected before the program runs.

> [!tip] Interview answer
> Static typing means the compiler knows the type of every variable and expression and rejects operations that type does not allow. Java is also strongly typed: a variable cannot hold an arbitrary bit pattern. A reference can still point at a subclass instance, which is how polymorphism works, while casts and array stores remain run-time checks. `var` and generics do not change that model.
