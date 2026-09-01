<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS

# What is the initial number of buckets in a `HashMap`?

> [!abstract] Short answer
> **16, for `new HashMap()`.** That is the default **initial capacity** (bucket count), with load factor 0.75. Other constructors set a different capacity; OpenJDK rounds it up to a **power of two**. It is not `size()`, and it is not “room for that many keys” unless you use `HashMap.newHashMap(n)` (Java 19+).

## Default 16; otherwise what you pass, rounded

`HashMap()` javadoc (Java SE 21): empty map, default initial capacity **(16)** and default load factor **(0.75)**. `HashMap(int initialCapacity)`: that capacity, load factor 0.75. `HashMap(int, float)`: both. Capacity is the number of **buckets** at creation. Negative capacity throws `IllegalArgumentException`. [[What are the initial capacity and load factor parameters of HashMap]]

OpenJDK: `table` is allocated **lazily** on first use; length is always a power of two. `tableSizeFor(cap)` rounds the requested capacity up (`HashMap(20)` → 32 buckets). The implementation maximum is `1 << 30`. You cannot have 15 buckets. [[What is the internal structure of HashMap]] [[What is initial capacity in Java collections such as HashMap]]

```java
new HashMap<String, Integer>();           // 16 buckets, load 0.75
new HashMap<String, Integer>(32);         // 32 buckets, load 0.75
new HashMap<String, Integer>(20);         // 32 buckets after tableSizeFor(20)
HashMap.newHashMap(20);                   // capacity for ~20 mappings at 0.75
```

**Listing 1.** Default vs requested capacity. `newHashMap(20)` is **not** “20 buckets.”

```d2
direction: down
ctor: "which constructor?" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
def: "HashMap()\n16 buckets" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
n: "HashMap(n)\n≥ n, power of two" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}

ctor -> def: no-arg
ctor -> n: int / int+float
```

**Fig. 1.** “Initial number of buckets” is 16 only for the no-arg constructor.

Resize later **doubles** the table when `size` exceeds capacity × load factor (24 entries for 16 × 0.75). Iteration cost is capacity + size, so starting at 16 is the usual default; a huge `initialCapacity` makes empty walks expensive. [[What rule governs when HashMap grows its number of buckets]]

> [!warning] “Arbitrary” capacity is not “any integer of buckets”
> Parameterized constructors take a **requested** bucket count, not a free-form table length: non-negative, rounded to a power of two, capped. Passing `size()` of a collection as `initialCapacity` still resizes around 0.75 occupancy. For “I will insert n mappings,” `newHashMap(n)` is the API.

> [!tip] Interview answer
> **The no-arg `HashMap` starts with 16 buckets and load factor 0.75. Other constructors let you set initial capacity, which the JDK rounds up to a power of two. That number is buckets, not how many keys you can put before a resize.**
