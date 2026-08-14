<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/String #SRS

# Why can two unequal objects share the same `hashCode` value?

> [!abstract] Short answer
> Because the contract does not require distinct hashes for unequal objects. `hashCode` returns an `int`, so there are only 2³² possible values, while there are far more objects. A hash table uses the integer only to pick a candidate bin; it still decides membership with identity or `equals`. A shared hash is a collision, not a proof of equality.

## The contract allows it

`Object.hashCode` requires equal objects to share a hash. It does **not** require the converse. Unequal objects may return the same integer; distinct hashes are recommended only because they usually make hash tables faster. [[How would you explain the hashCode method contract in Java]] is that three-clause rule; this card is the third clause.

```d2
direction: down
eq: "a.equals(b) == true" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
must: "Must share hashCode" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
uneq: "a.equals(b) == false" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
may: "May share hashCode\n(collision is legal)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}

eq -> must
uneq -> may
```

**Fig. 1.** Equality implies equal hashes. Unequality does not imply different hashes.

Pigeonhole makes collisions inevitable for any `int` hash as soon as more than 2³² distinct values exist. Even before that bound, an implementation may return a constant and still obey the contract.

## A specified `String` collision

`String.hashCode` is defined as `s[0]*31^(n-1) + s[1]*31^(n-2) + … + s[n-1]` using `int` arithmetic. For two-character strings that is `31 * s[0] + s[1]`:

```text
"Aa": 31 * 65 + 97 = 2112
"BB": 31 * 66 + 66 = 2112
```

**Listing 1.** Conceptual evaluation of the published `String` formula. The strings are unequal, yet the hashes match.

```java
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        String a = "Aa";
        String b = "BB";

        System.out.println("equals=" + a.equals(b));
        System.out.println("sameHash=" + (a.hashCode() == b.hashCode()));
        System.out.println("hash=" + a.hashCode());

        Map<String, String> map = new HashMap<>();
        map.put(a, "first");
        map.put(b, "second");

        System.out.println("getAa=" + map.get("Aa"));
        System.out.println("getBB=" + map.get("BB"));
        System.out.println("size=" + map.size());
    }
}
```

**Listing 2.** Java 8+ run of that collision. `HashMap` still stores two mappings: after the hashes match, it compares the keys. See [[Is equals invoked when a HashMap bucket contains a single element]] and [[When does a hashCode collision occur in a HashMap]].

> [!warning] Collision is not equality
> `sameHash=true` does not let you skip `equals`. If a map treated equal hashes as equal keys, `"Aa"` would overwrite `"BB"`. It does not: `size` stays `2`. The opposite mistake is also common: claiming two objects with the same hash must be equal, or that a collision is a JVM bug. [[What is a hash collision]] is the general name for this event.

A second, independent way two unequal keys share a **bucket** is a different raw `hashCode` that still maps to the same index after spreading and `hash & (n - 1)`. That is a bucket collision, not necessarily a `hashCode` collision. This card is only about equal `hashCode()` values.

> [!tip] Interview answer
> **Unequal objects may share a `hashCode` because the contract never required uniqueness, and an `int` cannot uniquely label every object. Hash tables tolerate that: they use the hash to choose a bin, then `equals` to tell keys apart. `"Aa"` and `"BB"` are a standard `String` example: different text, hash `2112`, two map entries.**
