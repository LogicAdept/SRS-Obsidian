<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Contract #SRS

# How would you explain the `hashCode` method contract in Java?

> [!abstract] Short answer
> `hashCode` returns an `int` that hash tables use to group candidates. During one run of an application it must return the same integer while equality-relevant state is unchanged. If `a.equals(b)` is `true`, `a.hashCode()` and `b.hashCode()` **must** be equal. Unequal objects **may** share a hash code; that is a legal collision, not a contract violation.

## The three required rules

1. **Consistency in one execution.** Repeated calls on the same object return the same `int` while information used by `equals` is unmodified. The value need not be the same in a later run of the same application.
2. **Equal objects, equal hashes.** `equals` true implies equal hash codes. This is the rule that makes hash-based lookup sound.
3. **Unequal objects need not differ.** Distinct hashes for unequal objects usually improve hash-table speed, but they are not required. A constant `hashCode` still satisfies the contract.

The inherited `Object.hashCode` aims, as far as is reasonably practical, to return distinct integers for distinct objects. That is an implementation goal for identity equality, not a requirement you must copy when you override. See [[What is the Object equals contract]] and [[How would you explain the equals and hashCode contract together in Java]].

> [!warning] The implication is one-way
> Same hash does not mean `equals` is true. [[Why can two unequal objects share the same hashCode value]] is exactly this clause. Treating a collision as a bug is the usual interview mistake.

## How a hash table uses the integer

```d2
direction: down
hash: "hashCode() -> int" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
bin: "HashMap spreads the int\nand selects a bin" {
  width: 280
  height: 85
  style.fill: "#e3f2fd"
}
stored: "Compare stored node hash" {
  width: 260
  height: 75
  style.fill: "#fff3e0"
}
eq: "Then identity or equals" {
  width: 260
  height: 75
  style.fill: "#e8f5e9"
}

hash -> bin
bin -> stored
stored -> eq
```

**Fig. 1.** The hash only chooses a candidate set. `HashMap` still checks the stored hash, then identity or `equals`. Constant-time `get`/`put` is documented only when hashes disperse keys among bins.

Many keys with the same `hashCode()` slow any hash table. In Java 8+, a crowded bin may become a tree, and when keys are `Comparable` the map may use comparison order to break ties. That is a performance mitigation, not a change to the `hashCode` contract. See [[When does a hashCode collision occur in a HashMap]].

## Equal hashes may still identify different keys

```java
import java.util.HashMap;
import java.util.Map;

public class Main {
    static final class Bucket {
        final int id;
        final int hash;

        Bucket(int id, int hash) {
            this.id = id;
            this.hash = hash;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Bucket)) return false;
            Bucket other = (Bucket) o;
            return id == other.id;
        }

        @Override
        public int hashCode() {
            return hash;
        }
    }

    public static void main(String[] args) {
        Bucket first = new Bucket(1, 7);
        Bucket equal = new Bucket(1, 7);
        Bucket colliding = new Bucket(2, 7);

        System.out.println("equalObjects=" + first.equals(equal));
        System.out.println("equalHashes=" + (first.hashCode() == equal.hashCode()));
        System.out.println("unequalObjects=" + first.equals(colliding));
        System.out.println(
                "collisionLegal=" + (first.hashCode() == colliding.hashCode())
        );
        System.out.println("consistent=" + (first.hashCode() == first.hashCode()));

        Map<Bucket, String> map = new HashMap<>();
        map.put(first, "A");
        map.put(colliding, "B");

        System.out.println("getEqual=" + map.get(equal));
        System.out.println("size=" + map.size());
    }
}
```

**Listing 1.** Java 8+ illustration of the contract. Equal `id` values share a hash and retrieve the same mapping. Unequal `id` values may still share hash `7`; `HashMap` keeps both mappings (`size` is `2`).

If `Bucket` used `id` for `equals` but a different, unstable field for `hashCode`, two equal instances could disagree on the integer and break rule 2. [[Why should equals and hashCode be overridden together]] is that failure mode. Changing equality-relevant state after insertion is a separate, unspecified-map problem; see [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]].

The return type is `int`, so every `int` value is a legal hash. Distribution quality is a performance concern, not a range restriction. [[What range of int values can hashCode return in Java]] and [[What steps must you follow to implement hashCode correctly]] cover those details.

> [!tip] Interview answer
> **`hashCode` must be stable while `equals` state is unchanged, and equal objects must share the same integer. Unequal objects are allowed to collide. Hash tables use the integer only to pick a bin; they still confirm the key with identity or `equals`. Distinct hashes help speed, but they are not required by the contract.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего нужен метод `hashCode()`?**

Метод `hashCode()` необходим для вычисления хэш кода переданного в качестве входного параметра объекта. В Java это целое число, в более широком смысле - битовая строка фиксированной длины, полученная из массива произвольной длины. Этот метод реализован таким образом, что для одного и того же входного объекта, хэш код всегда будет одинаковым. Следует понимать, что в Java множество возможных хэш кодов ограничено типом `int`, а множество объектов ничем не ограничено. Из-за этого, вполне возможна ситуация, что хэш коды разных объектов могут совпасть:

+ если хэш коды разные, то и объекты гарантированно разные;
+ если хэш коды равны, то объекты могут не обязательно равны.
