<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What is the difference between `IndexOutOfBoundsException` and `ArrayIndexOutOfBoundsException`?

> [!abstract] Short answer
> **`IndexOutOfBoundsException` is the general unchecked type for an index that is out of range.** **`ArrayIndexOutOfBoundsException` is the array-specific subclass.** `StringIndexOutOfBoundsException` is the string-specific subclass. `List.get` / `set` throw the **parent**, not the array type.

## Parent for any index, subclass for arrays

`IndexOutOfBoundsException` extends `RuntimeException`. It marks an index of some sort — array, string, or list-like structure — that is out of range. Applications may subclass it for similar cases ([[What is RuntimeException]], [[Is RuntimeException a subclass of Exception]]).

`ArrayIndexOutOfBoundsException` extends that parent. The JVM throws it for an array access whose index is negative or `>= length` ([[What is ArrayIndexOutOfBoundsException]]).

`StringIndexOutOfBoundsException` is the other JDK subclass. `String.charAt` throws it when the index is negative, **or greater than or equal to** the string’s length (`charAt(s.length())` throws).

`List.get` and `List.set` document `IndexOutOfBoundsException` (`index < 0 || index >= size()`). They do **not** throw `ArrayIndexOutOfBoundsException`.

`catch (IndexOutOfBoundsException e)` matches both subclasses. A later `catch (ArrayIndexOutOfBoundsException e)` is unreachable ([[What is an unreachable catch block error]], [[Can you catch an unchecked exception in Java]]).

```d2
direction: down
rte: RuntimeException {
  width: 220
  height: 40
}
ioob: IndexOutOfBoundsException {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
aioob: ArrayIndexOutOfBoundsException {
  width: 300
  height: 40
  style.fill: "#ffebee"
}
sioob: StringIndexOutOfBoundsException {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
rte -> ioob
ioob -> aioob
ioob -> sioob
```

**Fig. 1.** Array and string types are subclasses of the general index exception.

```java
import java.util.List;

class Demo {
    static int arrayPastEnd() {
        int[] a = new int[4];
        return a[4];
    }

    static char charAtLength() {
        return "ab".charAt(2);
    }

    static String listGet() {
        return List.of("a").get(1);
    }
}
```

**Listing 1.** `arrayPastEnd` throws `ArrayIndexOutOfBoundsException`. `charAtLength` throws `StringIndexOutOfBoundsException`. `listGet` throws `IndexOutOfBoundsException`. All three are unchecked; none needs `throws` ([[Must you declare RuntimeException in a throws clause]]). A null array is `NullPointerException`, not a bounds type ([[What is NullPointerException]]).

> [!warning] `catch (IndexOutOfBoundsException)` already covers arrays
> `ArrayIndexOutOfBoundsException` is a subclass. Catch the parent if you want every bad index. Catching the array type after the parent is an unreachable-catch error ([[What is an unreachable catch block error]]).

> [!warning] `charAt` is not `ArrayIndexOutOfBoundsException`
> Strings are not arrays at the language level for this throw. `s.charAt(s.length())` is `StringIndexOutOfBoundsException`. `List.get` is the parent, not the array subclass.

> [!tip] Interview answer
> **`IndexOutOfBoundsException` is the general unchecked bad-index type.** Arrays throw the subclass `ArrayIndexOutOfBoundsException`; `String.charAt` throws `StringIndexOutOfBoundsException`; `List.get` throws the parent. Catching the parent also catches the array subclass.
