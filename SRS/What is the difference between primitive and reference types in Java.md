<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #DataAndState/ValueSemantics #DataAndState/ReferenceSemantics #SRS

# What is the difference between primitive and reference types in Java?

> [!abstract] Short answer
> **A primitive variable holds the value; a reference variable holds a pointer (or `null`).** The eight primitive types are `byte`, `short`, `int`, `long`, `char`, `float`, `double`, and `boolean`. Every other type is a reference type: class, interface, array, or type variable. Assignment and argument passing **copy the slot** — so primitives are copied, objects are **shared** through copied pointers.

## Two kinds of type, two kinds of value

The language has primitive types and reference types ([[How would you explain Java data types primitives and references]]). A primitive value *is* the number, character, or `true`/`false`. There is no object header, no `null`, and no instance method on the value itself ([[How would you explain Java primitive data types]]).

A reference value is either `null` or a pointer to an **object**: a class instance or an array ([[How would you explain reference types in the Java type system]]). `int[]` is a reference type even when its cells are `int`. Wrappers (`Integer`) are objects; unboxing yields a primitive.

`==` / `!=` on primitives compare bits of the value (with the usual NaN caveats). On references they compare **identity** — same object, not equal contents.

Defaults follow the same split: numeric/`char`/`boolean` fields get zero/`'\u0000'`/`false`; reference fields get `null`.

```d2
direction: down
prim: "int n = 1\nslot holds 1" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
ref: "Point p\nslot holds pointer" {
  width: 180
  height: 60
}
heap: "Point instance" {
  width: 150
  height: 40
  style.fill: "#fff8e1"
}

ref -> heap: "points to"
```

**Fig. 1.** Copying `n` copies `1`. Copying `p` copies the pointer; both names see one instance.

```java
public final class PrimitiveVsReference {
    static void bump(int n, int[] cells) {
        n++;
        cells[0]++;
    }

    public static void main(String[] args) {
        int n = 1;
        int[] cells = { 1 };
        bump(n, cells);
        System.out.println(n);         // 1  (copy of the int)
        System.out.println(cells[0]);  // 2  (same array object)
    }
}
```

**Listing 1.** The `int` parameter is a copy. The `int[]` parameter is a copy of the **reference**; the array on the heap is shared.

> [!warning] Wrappers and `==` lie next to primitives
> `Integer a = 1000; Integer b = 1000;` can be `a != b` even though both unbox to 1000: `==` on `Integer` is identity. A method cannot change the caller’s `int` by assigning to the parameter; mutating a shared object through a reference can. `null` is legal only for references.

> [!tip] Interview answer
> **Primitives store the value; references store a pointer or `null`.** Passing or assigning copies the variable’s slot, so ints are duplicated and objects are aliased. Arrays and wrappers are objects, even when they carry primitive cells.
