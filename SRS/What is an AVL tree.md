<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Tree/AVL #SRS

# What is an AVL tree

> [!abstract] Short answer
> A **self-balancing binary search tree** named for its inventors Adelson-Velskii and Landis. Its one extra invariant on top of BST order: for **every** node, the heights of the left and right subtrees differ by **at most 1**. That invariant forces the depth to stay `O(log n)`, so search, insert and delete are all `O(log n)` worst case. Violations found after an update are repaired by **rotations**.

## Balance invariant and the four rotation cases

Without balancing, a BST degrades to a linked list under sorted insertions and lookups become `O(n)`. AVL keeps every node's balance factor in `{ -1, 0, +1 }`; an insert or delete can push one ancestor to ±2, and exactly one of four cases applies — extra node in the **left child of the left** child (single right rotation), **right child of the right** child (single left rotation), **left child of the right** child (double), or **right child of the left** child (double). An insertion needs at most one single or double rotation; a deletion can cascade rotations up the ancestor path, which is the price of the strict balance.

```java
// Single right rotation around unbalanced node z (conceptual):
Node y = z.left;                 // y becomes the new subtree root
z.left = y.right;                // y's right subtree moves under z
y.right = z;                     // z drops to y's right
updateHeight(z); updateHeight(y);
return y;                        // BST order is preserved throughout
```

**Listing 1.** The left-left case: one rotation lowers the taller side by one level and raises `y`, restoring every affected balance factor. The mirror case rotates left.

## AVL versus red-black — and where each lives

AVL's stricter invariant makes its shape flatter than a red-black tree's, so **lookups are a bit faster**, while updates pay for it with more rotations. Engineering took the update-friendlier side for libraries: Java's `TreeMap` and `TreeSet` are red-black trees, not AVL — a fact worth stating precisely before anyone asks how [[Compare HashMap and TreeMap tradeoffs]] plays out at the structure level, or what happens to that balance when [[What happens if you mutate a TreeMap key after insertion]] breaks the ordering. AVL remains the textbook answer for read-heavy ordered sets and lives on in databases and teaching material alongside [[Can TreeMap have null keys or null values]] clarifications of the shipped alternatives.

> [!warning] "TreeMap is an AVL tree" is the classic miss
> Interviewers hear this constantly: `TreeMap`/`TreeSet` in the JDK are **red-black** trees — a looser balance that guarantees height `≤ 2·log(n)`, not AVL's `≈ 1.44·log(n)` bound. The second trap is the word "balanced": AVL is not perfectly balanced (that would demand every level full), it is balanced *within one level of height difference per node*.

> [!tip] Interview answer
> AVL is a BST where every node's subtree heights differ by at most one — that alone caps depth at O(log n), so search, insert and delete are logarithmic worst case. Updates repair the invariant with rotations: at most one single or double rotation per insert, cascades possible on delete. It balances more strictly than red-black — faster lookups, costlier updates — which is why the JDK picked red-black for TreeMap and TreeSet.
