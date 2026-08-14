<!--
reps: 0
priority: 0
-->
#Java/Collections/List #Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #Java/Collections/Set/HashSet #SRS

# What is initial capacity in Java collections such as `HashMap`?

> [!abstract] Short answer
> **A constructor argument that sizes internal storage before the first growth.** It is **not** `size()`. For `ArrayList` / `Vector` it is the length of the element array (slots for elements). For `HashMap` / `HashSet` / `Hashtable` it is the number of **buckets**, and a load factor still sits between buckets and how many keys you can insert. Same name, different unit. HashMap knobs: [[What are the initial capacity and load factor parameters of HashMap]].

## Same word, two machines

`ArrayList` javadoc: capacity is the size of the array used to store the elements; it is always at least the list size. Default no-arg list: initial capacity **ten**. `ensureCapacity` can raise it before a bulk add so you do less reallocation. `Vector()` uses an internal array of size **10**. Growth policy of `ArrayList` is otherwise unspecified beyond amortized constant-time `add`.

```text
ArrayList / Vector     capacity = element-array length
                       new ArrayList<>(100) holds 100 elements before grow

HashMap / HashSet      capacity = bucket count
                       new HashMap<>(100) is 100 buckets, not 100 keys
                       load factor 0.75 still applies

Hashtable              buckets too; default capacity 11, load 0.75
HashSet                the int is the backing HashMap's capacity
```

**Listing 1.** Defaults from the class javadocs (Java SE 21): `ArrayList` 10, `HashMap`/`HashSet` 16, `Hashtable` 11.

```d2
direction: down
n: "new C(n)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
list: "ArrayList\nn element slots" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
map: "HashMap / HashSet\nn buckets\nkeys ≈ n × loadFactor" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
n -> list
n -> map
```

**Fig. 1.** Passing the expected **element count** as `HashMap`/`HashSet` capacity still rehashes. Use `HashMap.newHashMap` / `HashSet.newHashSet` (since 19) when you have a count of mappings or elements.

`HashSet` iteration cost is size **plus** backing-map capacity, same warning as `HashMap`: do not set initial capacity too high (or load factor too low) if you iterate. `TreeMap` and `LinkedList` are not hash tables or resizable arrays; they have no this-style capacity constructor.

Negative capacity is `IllegalArgumentException` on `ArrayList`, `HashMap`, `HashSet`, `Hashtable`, `Vector`.

> [!warning] `new HashSet<>(list.size())`
> That sizes **buckets** of the inner `HashMap`. For `list.size()` elements at load 0.75 it is still too small. `newHashSet(list.size())` is the API that means “this many elements.”

> [!tip] Interview answer
> **Initial capacity pre-sizes storage; it is not the current size. On `ArrayList` it is array slots (default 10). On `HashMap`/`HashSet` it is buckets (default 16), so expected keys need the load factor or `newHashMap`/`newHashSet`. `Hashtable` defaults to 11 buckets.**
