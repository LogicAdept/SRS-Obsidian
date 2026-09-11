<!--
reps: 0
priority: 0
-->
#Databases #Caching #SystemDesign/Performance #SRS

# What is cold data and hot data

> [!abstract] Short answer
> Hot data is the working set accessed constantly right now; cold data is everything accessed rarely or never after it ages. The split is temporal, not structural: the same row is hot the day it is written and cold a year later. Systems exploit the split by tiering storage — hot data on fast media and in caches, cold data on cheap, slower storage with its own retention rules.

## Why the split matters

Storage economics force the decision: RAM and NVMe are expensive per gigabyte, HDD and object storage are cheap but slow. If 1% of rows absorb 90% of reads — a typical skew — keeping the whole dataset on the fast tier wastes 99% of its capacity. So designs separate tiers: an in-memory or SSD-backed hot layer (caches, recent partitions), and a cold layer (compressed old partitions, S3 archive classes). Databases expose the seam directly: PostgreSQL partitioning by range lets old months live in cheaper tablespaces or be archived, ClickHouse TTL rules move parts between storage policies, and object stores offer retrieval-tiered classes. The cache side is the same idea at smaller scale — a cache holds the hot subset, which is why [[How would you explain cache hit rate and cache miss rate]] is the health metric of the split: a shrinking working set or bad eviction shows up as falling hit rates. [[When is caching useful and when is it dangerous]] covers the read-side decision; [[What problem does database sharding solve]] is the write-side complement.

## Moving data between temperatures

Tiering is a policy question: what makes data cold? Usually time (age since write), sometimes event (order shipped, user churned) or volume (partitions roll over). Concrete mechanisms: TTL-based expiry and tiered storage rules (ClickHouse `TTL ... TO VOLUME`/`TO DISK`, Redis eviction for the memory tier), time-based table partitioning with archival jobs (PostgreSQL, MySQL), and lifecycle rules on object storage. The policy must also decide writability: cold tiers are often read-only or append-only, which is fine for audit logs and history but wrong for data that still mutates. [[What difficulties arise when working with caching]] explains what happens when the hot tier is sized wrong; the partitioning companion [[How does vertical partitioning differ from horizontal partitioning]] distinguishes row-range cooling from column-level separation.

> [!warning] Cooling is a one-way door if you plan queries badly
> Queries that must scan "everything" (global aggregations across hot and cold tiers) get slower and more expensive once cold data moves to slow media or an archive class. Decide access patterns before cooling, or keep a compact aggregate table that survives the move.

> [!tip] Interview answer
> Hot data is the current working set — cache it on fast media; cold data is aged history — archive it on cheap storage with TTL and lifecycle rules. The split follows access skew: a small hot fraction carries most reads, so tiering buys speed where it matters and capacity where it doesn't.
