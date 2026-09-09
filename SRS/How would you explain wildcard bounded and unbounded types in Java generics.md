<!--
reps: 0
priority: 0
-->
#Java/Generics #SRS

# How would you explain wildcard bounded and unbounded types in Java generics

> [!abstract] Short answer
> A wildcard `?` is an unknown type argument. `List<?>` means a list of some fixed but unknown type; `List<? extends Number>` means some unknown type that is `Number` or a subtype; `List<? super Integer>` means some unknown supertype of `Integer`. Wildcards create subtype relations between parameterized types that generics otherwise deny, and they set what you may read and write.

Because generics are invariant, `List<Integer>` is not a `List<Number>`. Wildcards are the use-site mechanism that restores flexible subtyping: `List<Integer>` **is** a `List<? extends Number>` and a `List<?>`. The three forms differ in what the unknown type could be, and the compiler derives read/write permissions from that.

## The three wildcard forms

`?` is equivalent to `? extends Object`: every parameterization matches. `? extends B` bounds the unknown from above — the actual argument is some subtype of `B`. `? super B` bounds it from below — the actual argument is `B` or one of its supertypes. The unknown is fixed per object: one `List<? extends Number>` variable may first reference a `List<Integer>` and later a `List<Double>`, but a single list object it references does not mix element types.

```d2
direction: right
li: "List<Integer>" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
ld: "List<Double>" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
ln: "List<Number>" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
ext: "List<? extends Number>\n(read as Number)" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
sup: "List<? super Integer>\n(write Integer)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
any: "List<?>\n(read as Object)" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
li -> ext: subtype of
ld -> ext: subtype of
li -> sup: subtype of
ln -> sup: subtype of
li -> any: subtype of
ld -> any: subtype of
ln -> any: subtype of
```

**Fig. 1.** Wildcard parameterizations sit above concrete ones: every concrete list is a subtype of the matching wildcard types.

## Reads and writes each form allows

Reading from `? extends Number` is safe because whatever the element type is, it is a `Number`. Writing is blocked because the compiler cannot know which subtype the list actually holds — only `null` is allowed, since it belongs to every reference type. `? super Integer` is the mirror: writing an `Integer` is safe for any supertype list, while reading can only promise `Object`.

```java
import java.util.ArrayList;
import java.util.List;

public class WildcardDemo {

    static double sum(List<? extends Number> nums) {
        double total = 0;
        for (Number n : nums) total += n.doubleValue(); // read: every element is a Number
        return total;
        // nums.add(1);  // compile-time error: no safe write into ? extends
        // nums.add(null); // the only permitted write
    }

    static void seed(List<? super Integer> sink) {
        sink.add(1);  // write: Integer (and subtypes) always fit
        sink.add(2);
        // Integer x = sink.get(0); // compile-time error: only Object is guaranteed
    }

    static void printAll(List<?> any) {
        for (Object o : any) System.out.print(o + " "); // read as Object
    }

    public static void main(String[] args) {
        List<Integer> ints = new ArrayList<>(List.of(1, 2, 3));
        List<Double> doubles = new ArrayList<>(List.of(0.5, 1.5));
        System.out.println(sum(ints));    // 6.0
        System.out.println(sum(doubles)); // 2.0

        List<Number> nums = new ArrayList<>();
        seed(nums);
        System.out.println(nums); // [1, 2]

        List<Object> objs = new ArrayList<>();
        seed(objs); // List<Object> is a List<? super Integer>

        printAll(ints); // 1 2 3
        System.out.println();
        System.out.println(ints instanceof List<?>); // true, ? is reifiable
    }
}
```

**Listing 1.** `? extends` reads, `? super` writes, `?` reads as `Object` — and only `null` ever goes into an upper-bounded list.

## Capture: turning `?` back into a workable type

Inside a method taking `List<?>`, the compiler treats each element as some unknown-but-fixed type **captured** per call. You cannot name that type, but a private generic helper can: `static <T> void reverse(List<T> list)` accepts `List<?>` by capture conversion, which is exactly how `Collections.reverse(List<?>)` is written. The get-and-put asymmetry here is the raw material for [[What is the difference between extends and super wildcards in Java generics]] and [[How would you explain the PECS rule for generic method signatures]].

> [!warning] `List<?>` is not `List<Object>`
> A `List<Object>` variable accepts any `List<Object>` object and you may `add` anything into it. A `List<?>` variable accepts lists of **any element type**, but you cannot add non-null elements to it — the unknown could be `List<String>`, and an `Integer` would corrupt it. Confusing the two is the classic wildcard lie; `instanceof List<?>` works precisely because unbounded wildcards are reifiable, unlike `List<Object>` checks after [[How does type erasure work for Java generics]].

> [!tip] Interview answer
> Wildcards parameterize a use site with an unknown type: unbounded `?` means any parameterization, `? extends B` some subtype of `B`, `? super B` some supertype of `B`. They are what makes `List<Integer>` a subtype of `List<? extends Number>` even though generics are invariant. Reading from `extends` is safe, writing only `null`; `super` accepts `B` and reads only as `Object`. And `List<?>` is not `List<Object>` — the first is any list, the second is one specific element type.

