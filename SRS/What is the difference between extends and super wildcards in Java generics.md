<!--
reps: 0
priority: 0
-->
#Java/Generics/TypeBounds #SRS

# What is the difference between extends and super wildcards in Java generics

> [!abstract] Short answer
> `? extends T` is an unknown **subtype** of `T`: you can read elements as `T`, but cannot add anything except `null`. `? super T` is an unknown **supertype** of `T`: you can add `T` values, but reading only guarantees `Object`. The compiler allows exactly the direction that cannot corrupt the actual runtime list.

Both wildcards create flexibility over invariance: `List<Integer>` is a `List<? extends Number>` and a `List<? super Integer>`, though it is neither a `List<Number>` nor a `List<Object>`. What differs is which operations stay type-safe for an unknown actual type.

## Reading from extends, writing to super

With `List<? extends Number>` the actual list may be `List<Integer>`, `List<Double>`, or anything else numeric — so every element **is** a `Number` and reading is safe, while `add(1)` must fail: if the list is really a `List<Double>`, an `Integer` would corrupt it. With `List<? super Integer>` the actual list may be `List<Integer>`, `List<Number>`, or `List<Object>` — all three accept an `Integer`, so writing is safe, but a read can only promise `Object` because the element could be any supertype.

```d2
direction: right
ext: "List<? extends Number>\nunknown subtype of Number" {
  width: 330
  height: 100
  style.fill: "#e8f5e9"
}
read: "Read: Number n = get(i)\nAlways safe" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
writeOff: "Write: add(1) rejected\n(null still allowed)" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
sup: "List<? super Integer>\nunknown supertype of Integer" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
put: "Write: add(42) accepted\nInteger fits every supertype" {
  width: 320
  height: 90
  style.fill: "#e3f2fd"
}
readObj: "Read: only Object\npromised" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}
ext -> read
ext -> writeOff
sup -> put
sup -> readObj
```

**Fig. 1.** Each wildcard opens one direction: upper bounds produce values, lower bounds consume them.

```java
import java.util.ArrayList;
import java.util.List;

public class ExtendsSuperDemo {

    // Producer: the structure hands out T values. Reading is safe.
    static double total(List<? extends Number> src) {
        double sum = 0;
        for (Number n : src) sum += n.doubleValue();
        // src.add(1); // compile-time error: the actual list may be List<Double>
        return sum;
    }

    // Consumer: the structure absorbs T values. Writing is safe.
    static void fill(List<? super Integer> dst) {
        dst.add(42);
        // int x = dst.get(0); // compile-time error: only Object is guaranteed
        Object o = dst.get(0); // reading is still possible, typed Object
        System.out.println("read back as " + o.getClass().getSimpleName());
    }

    public static void main(String[] args) {
        List<Integer> ints = new ArrayList<>(List.of(1, 2));
        List<Double> doubles = new ArrayList<>(List.of(0.5));
        System.out.println(total(ints));    // 3.0
        System.out.println(total(doubles)); // 0.5

        List<Number> nums = new ArrayList<>();
        fill(nums);   // writes Integer 42 into List<Number>
        List<Object> objs = new ArrayList<>();
        fill(objs);   // Object is also a supertype of Integer
        System.out.println(nums); // [42]

        // Invariance in one line: List<Integer> is NOT a List<Number>
        // List<Number> wrong = ints; // compile-time error
    }
}
```

**Listing 1.** The producer method reads, the consumer method writes; each blocked operation is a compile-time error, not a runtime check.

## Edge cases worth naming

`null` goes into any `? extends` reference — it belongs to every reference type, which is why it is the single permitted write. Methods taking `Object` still work on `List<? extends Number>` (`contains(Object)`, `remove(Object)`), because `Object` is a valid argument regardless of the unknown element type. Reading from `? super T` is legal — as `Object`. The full read/write contract is used by [[How would you explain the PECS rule for generic method signatures]] to shape API signatures, while [[How would you explain wildcard bounded and unbounded types in Java generics]] covers the unbounded form.

> [!warning] The popular half-truths
> "You cannot read from `? super`" is false — you read, but typed `Object`. "You can write into `? extends`" is false — even adding to it through a `Number` variable is rejected; only `null` passes. And neither wildcard relaxes invariance of the underlying type: the list you pass stays exactly the class it was, the wildcard only widens what the **variable** can reference.

> [!tip] Interview answer
> `? extends T` means some unknown subtype: safe to read as `T`, safe to write only `null`, because the compiler cannot prove the actual list accepts any specific value. `? super T` means some unknown supertype: safe to write `T`, reads come back as `Object`. That is why producer parameters take `extends`, consumer parameters take `super`, and a method doing both needs the exact type.

