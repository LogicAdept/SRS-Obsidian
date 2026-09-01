<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Where is the authoritative reference for Java primitive types?

> [!abstract] Short answer
> The **Java Language Specification**, chapter **Types, Values, and Variables**, section **Primitive Types and Values** (4.2). That section defines the eight primitives, their ranges, and that `float`/`double` are IEEE 754 binary32/binary64. Wrapper `MIN_VALUE` fields and tutorials **repeat** those facts; they do not define the types. Use the JLS edition that matches the SE release you claim (this vault: SE 24).

## Language spec first; API and IEEE as satellites

JLS 4.2 splits primitives into `boolean` and numeric types; numeric types into integral (`byte`, `short`, `int`, `long`, `char`) and floating-point (`float`, `double`). 4.2.1 gives the integer ranges and UTF-16 `char`; 4.2.3 / 4.2.4 cover IEEE values and operations (Java SE 15+ uses IEEE 754-2019). Conversions and promotion live in chapter 5; operators in chapter 15; definite assignment in chapter 16. `char`’s UTF-16 story is JLS **Unicode** (3.1). The Java Virtual Machine Specification restates primitive kinds for the **runtime**; it does not replace the language definition. [[What is the value range of the Java int type]] and [[What is the value range of the Java byte type]] are 4.2.1; [[Why is the Java char type 16 bits]] is 3.1; [[Why is 0.1 plus 0.2 not equal to 0.3 in Java]] is 4.2.3.

```d2
direction: down
jls: "JLS Primitive Types and Values\n(defines the eight types)" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
sat: "IEEE 754 (via JLS)\nUnicode (JLS 3.1)\nJVMS (runtime)" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
api: "java.lang wrappers\nMIN_VALUE / SIZE / TYPE" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
not: "tutorials / blogs / dumps\nnot normative" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

jls -> sat
jls -> api
jls -> not
```

**Fig. 1.** Authoritative is the JLS section that names the primitives. Wrappers and IEEE are cited from there, not instead of it.

`Integer.MIN_VALUE` is specified to be −2³¹ because the **language** `int` has that range; quoting only the API answers “what constant holds the bound,” not “what is `int`.” Oracle’s “Primitive Data Types” tutorial is a teaching summary. Interview dumps and memory cards are not a spec. [[What are the wrapper types for Java primitives]] is the API side; [[What happens on integer overflow in Java]] is JLS integer operations; [[Is the Java char type signed or unsigned]] is 4.2.1; [[What is a compile-time constant in Java]] is JLS 4.12.4 / 15.29.

```java
public final class PrimitiveSpecAnchors {
    public static void main(String[] args) {
        // These constants document JLS ranges; they do not replace 4.2.
        System.out.println(Byte.MIN_VALUE);      // -128
        System.out.println(Short.MAX_VALUE);     // 32767
        System.out.println(Integer.MIN_VALUE);   // -2147483648
        System.out.println(Long.SIZE);           // 64
        System.out.println(Character.SIZE);      // 16
        System.out.println(Float.TYPE.getName());  // float
        System.out.println(Double.BYTES);        // 8
        System.out.println(Boolean.TYPE.getName()); // boolean
    }
}
```

**Listing 1.** Wrapper `MIN_VALUE` / `SIZE` / `TYPE` match the language types. For a dispute about the type itself, open JLS 4.2, not this listing.

> [!warning] “Oracle docs” is not one document
> The SE API, the JLS, the JVMS, and the tutorials all live under Oracle/OpenJDK documentation. For **what a primitive is**, cite **Primitive Types and Values**, not `Integer` JavaDoc and not a tutorial table. Do not treat IEEE 754 as a Java-only page — JLS 4.2.3 points at that standard for `float` and `double`.

> [!tip] Interview answer
> The authoritative reference is the Java Language Specification, Primitive Types and Values — chapter 4 of the JLS for your SE version. Wrapper constants and tutorials copy those ranges. If the question is runtime layout, add the JVM Specification; if it is decimal `0.1`, add IEEE 754 as the JLS already does.
