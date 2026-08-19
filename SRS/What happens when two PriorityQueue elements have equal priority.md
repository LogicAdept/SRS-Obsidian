<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: if multiple objects are present of the **same priority**, it can **poll any one of them randomly**.

> [!warning] Unverified traps from the dump
> - “Randomly” is dump wording — not a documented random shuffle; treat as **no FIFO tie-break** unless you add a comparator that breaks ties.
> - Duplicates are allowed; equal priority is not “only one survives” like `TreeSet`.
