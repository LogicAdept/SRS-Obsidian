<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Implementation #Java/Arrays #Java/Language/Records #Java/Versions/16 #SRS

# What steps must you follow to implement `hashCode` correctly?

> [!abstract] Short answer
> Override `public int hashCode()` together with `equals`, compute the `int` from **the same logical fields** `equals` uses, and keep it stable while that state is unchanged. Equal objects must get the same integer; unequal objects may collide. Prefer `Objects.hash` for several fields, `Objects.hashCode` for one nullable reference, type-specific `hashCode` for primitives, and `Arrays.hashCode` / `deepHashCode` for arrays.

## Satisfy the contract first

`hashCode` exists for hash tables. The three rules are: consistent in one run while `equals` state is unmodified; `equals` true implies equal hashes; unequal objects need not differ. [[How would you explain the hashCode method contract in Java]] is that list. The `equals` API note is that if you override `equals`, you generally must override `hashCode` as well. [[Why should equals and hashCode be overridden together]] is the failure mode.

```text
1. @Override public int hashCode()     // not a different signature
2. Same fields as equals               // or a subset; never a rogue extra field
3. Combine them into one int
4. Do not mutate those fields after the object is used as a hash-table key
```

**Listing 1.** Required process. Field choice is [[How would you explain which fields should be included when implementing hashCode in Java]].

## Combine fields with the platform helpers

`Objects.hash(x, y, z)` is specified for multi-field `Object.hashCode` implementations: it hashes as if the values were in an array passed to `Arrays.hashCode(Object[])`.

```java
@Override
public int hashCode() {
    return Objects.hash(x, y, z);
}
```

**Listing 2.** Documented pattern from `Objects.hash` (Java 7+).

> [!warning] `Objects.hash(oneRef)` is not `oneRef.hashCode()`
> With a **single** argument, `Objects.hash(o)` does **not** equal `o.hashCode()`. That value is `Objects.hashCode(o)` (null-safe: `0` when `o` is null). Using `Objects.hash(name)` for a one-field class is a legal but different mix and a common surprise.

For primitives, use the wrapper `hashCode` methods so `float`/`double` follow representation equivalence, matching `equals` that used `Double.compare` or `doubleToLongBits` rather than `==`. For a field that is an array, `arr.hashCode()` is identity; `Arrays.hashCode(arr)` (or `deepHashCode` when `equals` used `deepEquals`) is content. `Arrays.hashCode` is specified to agree with `Arrays.equals` on the same array type.

```java
@Override
public int hashCode() {
    int result = Integer.hashCode(id);
    result = 31 * result + Objects.hashCode(name);
    result = 31 * result + Arrays.hashCode(tags);
    return result;
}
```

**Listing 3.** Conceptual manual mix. Any `int` is legal, including negatives; see [[What range of int values can hashCode return in Java]]. `31 * result + field` is a common combiner, not a language requirement.

A `record` already provides `equals` and `hashCode` from its components. Do not override one of them without the other.

## After the integer exists

Keep the value stable while the object is a key of a `HashMap` / `HashSet`. Mutating an equals field after `put` is a lost-key problem, not a `hashCode` syntax error. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is that bug. Caching a hash on an immutable object is an optimization, not a contract requirement. A constant `return 0` is correct and slow.

> [!tip] Interview answer
> **Override `hashCode` whenever you override `equals`. Hash only equals-relevant state, with `Objects.hash` / `hashCode`, primitive `hashCode` methods, or `Arrays.hashCode`. Equal objects must match; collisions are allowed. Do not use `Objects.hash(single)` expecting `single.hashCode()`, and do not hash an array with `array.hashCode()` if `equals` compared contents.**
