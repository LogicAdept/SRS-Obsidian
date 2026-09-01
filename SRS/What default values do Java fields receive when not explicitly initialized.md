<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #DataAndState/ReferenceSemantics #SRS

# What default values do Java fields receive when not explicitly initialized?

> [!abstract] Short answer
> **Zeros, `false`, `'\u0000'`, or `null` — depending on the field’s type.** Numeric instance and class fields become `0` / `0L` / `0.0f` / `0.0d`, `boolean` becomes `false`, `char` becomes the NUL character, and every reference-typed field becomes `null`. **Local variables do not get these defaults.**

## Fields and array cells, not locals

When a class is initialized, its **class variables** (`static` fields) are created with a default. When an instance is created, its **instance variables** are created with a default. Array components get the same defaults when the array is created. That is the whole set ([[How would you explain what values initialized variable by default]]).

A local must be **definitely assigned** before use. `int n; System.out.println(n);` does not compile. There is no “field default” for a stack local.

Wrapper-typed fields are **references**, so they default to `null`, not to a boxed zero ([[What default values do wrapper-typed fields receive in Java]]).

| Field type | Default |
| --- | --- |
| `byte` / `short` / `int` | `0` |
| `long` | `0L` |
| `float` | `0.0f` (positive zero) |
| `double` | `0.0d` (positive zero) |
| `char` | `'\u0000'` |
| `boolean` | `false` |
| any reference (`String`, `Integer`, array type, …) | `null` |

```d2
direction: down
fields: "instance / static field" {
  width: 220
  height: 40
}
num: "0 / 0L / 0.0" {
  width: 140
  height: 40
}
bo: "false" {
  width: 80
  height: 40
}
ch: "'\\u0000'" {
  width: 100
  height: 40
}
ref: "null" {
  width: 80
  height: 40
}

fields -> num
fields -> bo
fields -> ch
fields -> ref
```

**Fig. 1.** Uninitialized **fields** take a type-shaped default. Locals do not.

```java
public class FieldDefaults {
    static int classInt;
    boolean flag;
    char c;
    Object ref;
    Integer boxed;

    public static void main(String[] args) {
        FieldDefaults x = new FieldDefaults();
        System.out.println(classInt);     // 0
        System.out.println(x.flag);       // false
        System.out.println((int) x.c);    // 0  ('\u0000')
        System.out.println(x.ref);        // null
        System.out.println(x.boxed);      // null, not Integer.valueOf(0)
        int local;
        // System.out.println(local);     // does not compile
    }
}
```

**Listing 1.** `static` and instance fields print their defaults. `boxed` is `null`. `local` is unusable until assigned.

> [!warning] `char` is NUL, `Integer` is `null`
> Printing a default `char` looks like an empty glyph, not `'0'`. A field of type `Integer` is not auto-boxed `0`; it is `null`, and unboxing it throws `NullPointerException`. Locals never receive this table.

> [!tip] Interview answer
> **Numeric fields: zero. `boolean`: `false`. `char`: `'\u0000'`. References: `null`.** That applies to instance fields, `static` fields, and array components. A local has no default; the compiler demands an assignment first.
