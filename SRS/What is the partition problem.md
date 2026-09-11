<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/DynamicProgramming/PartitionProblem #Problems/Optimization #SRS

# What is the partition problem

> [!abstract] Short answer
> The partition problem asks: given a multiset of positive integers, can it be split into two subsets with equal sums? Equivalently: is there a subset summing to total/2? It is NP-complete in general, but admits a classic pseudo-polynomial dynamic-programming solution — a boolean table over items and achievable sums — running in O(n · sum/2) time and optimizable to O(sum/2) space. Its intractability is the reason bin-packing-style schedulers and balancers use heuristics.

## The reduction that solves it

If the total S is odd, partitioning is immediately impossible. If S is even, a partition into two equal halves exists exactly when some subset sums to S/2 — the other elements then form the second half automatically. That reduction turns the problem into subset-sum for the target S/2, solvable by DP: a boolean array `dp` where `dp[s]` means "some subset of the items processed so far sums to s", initialized `dp[0] = true`; for each item `x`, update `dp[s] = dp[s] or dp[s-x]` iterating s downward (the downward order guarantees each item is used at most once — the 0/1 knapsack discipline; this problem IS 0/1 knapsack with value = weight = x and capacity S/2). The answer is `dp[S/2]`. Time O(n · S/2), space O(S/2) with the one-array trick; reconstructing the actual subsets adds parent tracking or a second pass over the table. The pseudo-polynomial caveat matters for the interview: the running time is polynomial in the numeric value of S, not in its bit length — which is exactly why the problem stays NP-complete despite this fast-in-practice algorithm (the polynomial-versus-pseudo-polynomial distinction is the natural follow-up).

```java
boolean canPartition(int[] a) {
    int S = 0; for (int x : a) S += x;
    if (S % 2 != 0) return false;          // odd total: impossible
    int half = S / 2;
    boolean[] dp = new boolean[half + 1];  // dp[s]: subset sums to s
    dp[0] = true;
    for (int x : a)
        for (int s = half; s >= x; s--)    // downward: use x once
            dp[s] |= dp[s - x];
    return dp[half];
}
```

**Listing 1.** The O(n·S/2) DP: odd total short-circuits; downward iteration enforces 0/1 usage.

## Complexity and where it appears

NP-completeness is proven by reduction from subset-sum (or equivalently 3-PARTITION-family problems), so no polynomial-time algorithm in bit length is known, and none is expected. The practical consequence: instances with small sums (or small n) are routinely solved exactly by the DP — realistic scheduler inputs often fall here — while adversarial or huge-sum instances need heuristics or approximations (greedy largest-first into the lighter half gives a 4/3-class guarantee for the balanced-partition objective; Karmarkar–Karp differencing does better in practice). The problem's fingerprints appear wherever a collection must be split into equal-work or equal-load halves: balancing partitions across two machines, two-player fair division of assets, cutting a workload between two nodes — the systems-level cousin is general load balancing and bin packing ([[What problem does database sharding solve]]'s shard-key balancing is the always-on engineering version, where heuristics and consistent hashing replace exact DP because the input changes continuously ([[How would you explain horizontal database sharding]]). Variants extend the DP unchanged: partition into k equal sums (3-partition is strongly NP-complete — harder in a precise sense), or minimize the difference between halves (the optimization version, same table, read the largest achievable s and report half − s... more precisely S/2 − s closest to S/2 from below).

> [!warning] Pseudo-polynomial is not polynomial
> The DP's loop count grows with the SUM's value, which is exponential in its bit length — a set of 30 items near 2^30 defeats it on memory alone even though n is small. Stating "we have a polynomial DP" instead of "pseudo-polynomial" is the classic complexity miss on this problem.

> [!tip] Interview answer
> Partition asks whether a multiset splits into two equal-sum subsets — reduce it to subset-sum for total/2 (odd total: no). Solve with a boolean DP over achievable sums in O(n·S/2) time and O(S/2) space, iterating sums downward for 0/1 usage. It is NP-complete — the DP is pseudo-polynomial — so real balancers use greedy or differencing heuristics for large-sum instances.
