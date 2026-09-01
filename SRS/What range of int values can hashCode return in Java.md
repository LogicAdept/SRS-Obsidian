<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Language/Primitives #SRS

# What range of `int` values can `hashCode` return in Java?

> [!abstract] Short answer
> **Any `int`:** from −2 147 483 648 to 2 147 483 647 inclusive. That is the full signed 32-bit range. The contract does not require a non-negative result, a positive result, or a value in `0 … nBuckets`. `0` and `Integer.MIN_VALUE` are legal hashes. Hash tables that index with bit masks already accept the whole range.

## The return type is `int`

`Object.hashCode` is declared `public int hashCode()`. An `int` is a 32-bit signed two’s-complement integer. Its values run from −2147483648 to 2147483647 inclusive (`Integer.MIN_VALUE` … `Integer.MAX_VALUE`). [[How would you explain the hashCode method contract in Java]] constrains **equality** of hashes, not which integers are allowed.

```text
hashCode() ∈ [Integer.MIN_VALUE, Integer.MAX_VALUE]
           = [-2147483648, 2147483647]
cardinality  2^32 = 4_294_967_296 distinct ints
NOT          2^32 as a maximum hash (that value is not an int)
NOT          2^31-1 as “how many hashes” (that is MAX_VALUE)
```

**Listing 1.** Every value of the `int` type is a legal hash. **2³²** is how many values exist, not a max hash. There is no extra “hash code range” in the language. More than 2³² pairwise-unequal objects **must** collide (pigeonhole). [[What happens to HashMap if all keys share the same hashCode]]

```d2
direction: down
fn: "hashCode() -> int" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
neg: "Negative\nincluding MIN_VALUE" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
z: "Zero" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
pos: "Positive\nthrough MAX_VALUE" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}

fn -> neg
fn -> z
fn -> pos
```

**Fig. 1.** Sign is not part of the contract. Quality of distribution is a performance concern, not a range restriction.

`String.hashCode` is specified with `int` arithmetic, so overflow is wraparound and the result is often negative. That is still a valid `hashCode`. [[Why can two unequal objects share the same hashCode value]] is why many strings also collide.

## Hash tables do not need you to force a positive `int`

`HashMap` mixes the raw `int` (`h ^ (h >>> 16)`) and then masks with `(n - 1) & hash`. Two’s-complement negatives participate in those bitwise operations; there is no “absolute value first” step in that path. [[When does a hashCode collision occur in a HashMap]] is about equal hashes, not about sign.

> [!warning] Do not `Math.abs` a hash to “make it positive”
> `Math.abs(Integer.MIN_VALUE)` returns `Integer.MIN_VALUE`, which is still negative. Using `Math.abs(hashCode()) % capacity` as a bucket index can therefore yield a negative index. The contract never asked for a non-negative hash. A constant `0` is also legal and merely a terrible distribution. “Maximum hashCode is 2³²” confuses **count** with **max value** (2³¹−1).

The inherited `Object.hashCode` tries, as far as is reasonably practical, to return distinct integers for distinct objects. “Distinct” still means distinct `int`s, including negatives. You may return any `int` when you override, as long as equal objects share that same integer. [[What steps must you follow to implement hashCode correctly]] is how to pick a value inside this range, not how to leave it.

> [!tip] Interview answer
> **`hashCode` may return any `int`, negatives included: −2 147 483 648 through 2 147 483 647 — 2³² distinct values, not a max of 2³². Zero is allowed. Hash tables mask bits themselves. Forcing `Math.abs` is unnecessary and breaks on `Integer.MIN_VALUE`.**
