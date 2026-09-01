<!--
reps: 0
priority: 0
-->
#Java/Arrays #Java/Language/Primitives #DataAndState/Objects #SRS

# Is a Java array a primitive or an object?

> [!abstract] Short answer
> **An object.** Arrays are dynamically created objects. You can assign an array to `Object`, call `Object` methods on it, and it has `length` and `clone`. The **component** type may be primitive (`int[]`) or a reference (`String[]`). The array itself is never a primitive.

## The array is the object; the slots may be primitives

Array types are reference types ([[How would you explain reference types in the Java type system]]). A variable of array type holds a **reference** to an array object. `int[] a;` does not allocate components; `a = new int[3]` does. Those three `int`s are primitive values inside a heap object ([[Can primitive values reside on the Java heap]]). Primitives are the eight types that are *not* objects ([[Which Java language constructs are not subclasses of java.lang.Object]]).

Members of an array type:

- `public final int length` — number of components (not part of the type; two `int[]`s may differ in length).
- `public clone()` — returns the same array type; a multidimensional clone is **shallow**.
- Every `Object` member except `Object.clone` (replaced by the array’s `clone`).

The associated `Class` object behaves as if the direct superclass were `Object` and the array implemented `Cloneable` and `Serializable`. `int[].class` is shared by every `int[]` of any length. The run-time name looks like `[I`, not a keyword type. `int.class.isPrimitive()` is true; `int[].class.isPrimitive()` is false and `isArray()` is true; `getComponentType()` is `int.class`. `Class.isPrimitive()` is also true for `void` — never for an array.

```d2
direction: down
arr: "int[] a" {
  width: 140
  height: 45
  style.fill: "#e3f2fd"
}
obj: "array object\nlength, clone, Object" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
cells: "components\nint, int, int" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}

arr -> obj: "reference"
obj -> cells
```

**Fig. 1.** The variable is a reference. The object is the array. The cells can still be primitives.

```java
public final class ArrayIsObject {
    public static void main(String[] args) {
        int[] ia = new int[3];
        Object o = ia;                    // arrays are Objects
        System.out.println(ia instanceof Object);
        System.out.println(ia.length);
        System.out.println(ia.getClass());           // class [I
        System.out.println(ia.getClass().getSuperclass());
        System.out.println(int.class.isPrimitive());          // true
        System.out.println(int[].class.isPrimitive());        // false
        System.out.println(int[].class.isArray());            // true
        System.out.println(int[].class.getComponentType() == int.class);

        int[] ib = new int[6];
        System.out.println(ia.getClass() == ib.getClass()); // true

        int[] copy = ia.clone();
        System.out.println(ia == copy);               // false

        // int primitive = ia;            // compile error: array is not int
        char[] chars = { 'h', 'i' };
        // String s = chars;              // compile error: char[] is not String
        System.out.println(o == ia);
        System.out.println(chars.length);
    }
}
```

**Listing 1.** `int[]` is an `Object` with `length` and `clone`. `char[]` is still an array object, not a `String`.

> [!warning] `int[]` is not an `int`, and `char[]` is not a `String`
> Component type primitive does not make the array a primitive. A `char[]` is mutable and is not NUL-terminated. `String` is a separate class ([[What is the difference between an array and an ArrayList]]). Indexing with `long` does not compile; indexes are `int` after promotion. `null` is a legal array reference; `a.length` on `null` is `NullPointerException`. Collections still cannot store a bare `int` ([[How does adding an int to an ArrayList of Integer autobox]]).

> [!tip] Interview answer
> **Arrays are objects, not primitives.** You assign them to `Object`, they have `length` and `clone`, and they inherit `Object`’s methods. `int[]` still stores `int` values in its slots. The array variable holds a reference; declaring it does not create the array.
