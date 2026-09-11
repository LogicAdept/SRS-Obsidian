<!--
reps: 0
priority: 0
-->
#SystemDesign #Career/Interview/Exercises #SRS

# How would you design Instagram

> [!abstract] Short answer
> An Instagram-class photo-feed system reduces to four services: media storage (original photos to blob storage, resized renditions generated async, served via CDN), a metadata store (photos, follows, likes — relational, sharded by user), a feed service (fan-out-on-write to precomputed per-user feed lists, with fan-out-on-read for celebrities), and identity/auth. The design conversation walks requirements → estimates → storage → feed generation → delivery, justifying each tradeoff: scale comes from CDN offload for media, sharding for metadata, and a hybrid feed model.

## Requirements, estimates, and media storage

Functional core: upload photos, follow users, generate a personalized feed, like and comment. Non-functional: read-heavy (orders of magnitude more feed reads than uploads), low media latency, high availability, eventual consistency tolerable for likes and feed freshness but not for account data. Ballpark sizing frames the storage talk: assume tens of millions of DAU, a few uploads per user per day, media averaging a few hundred KB plus renditions — media bytes dwarf metadata by orders of magnitude, so media must never sit in the database. The architecture follows the pattern Facebook's engineering organization built for exactly this problem: Haystack, the photo store described in the USENIX paper, serves tens of billions of photos by eliminating metadata lookups per photo — each image's name encodes its physical location, so a read touches disk once with all metadata held in main memory. The design lesson generalizes: originals go to blob storage, renditions (thumbnail, several sizes) are generated asynchronously on upload, and a CDN fronts everything — the origin serves cache misses only ([[What is caching used for]] and [[What is cold data and hot data]] cover the read-path logic).

```d2
direction: right
cdn: {
  label: "CDN\nmedia + feed cache\n(hit ratio targets the origin)"
  width: 210
  height: 90
}
api: {
  label: "API/stateless services\nauth | feed | upload"
  width: 210
  height: 80
}
meta: {
  label: "metadata DB\nusers, photos, follows\nsharded by user id"
  width: 230
  height: 80
}
media: {
  label: "blob store + renditions\n(async resize on upload)"
  width: 220
  height: 80
}
workers: {
  label: "async workers\nrenditions, fan-out"
  width: 180
  height: 70
}
api -> cdn: "serves"
cdn -> media: "miss"
api -> meta: "feed/likes"
api -> workers: "upload accepted"
workers -> media: "renditions"
```

**Fig. 1.** The four services: CDN-fronted media, sharded metadata, async workers for renditions and fan-out.

## Feed generation and the celebrity problem

Two feed models: fan-out-on-write (on upload, push the post into every follower's precomputed feed list — O(followers) work at upload, O(1) reads; perfect for ordinary users) and fan-out-on-read (assemble the feed at request time from followed users' latest posts — O(reads) work, no write amplification; required for accounts with millions of followers, where one upload would enqueue millions of writes). Real systems are hybrid: precomputed feeds for normal users, merge-at-read for celebrities, with the precomputed lists living in a cache tier (Redis-style key-value; the feed is exactly hot data — [[What difficulties arise when working with caching]] applies to the stampede when a popular account posts). Consistency is deliberately eventual: a like counter or a new follower appearing a second late is fine ([[What is eventual consistency]]), while identity and the photo's existence are strongly consistent — the metadata store shards by user id so a user's photos, follows and feed lists co-locate on one shard ([[How would you explain horizontal database sharding]]; identifiers themselves are the Long-versus-UUID question of [[When should you use Long versus UUID as identifiers]]). Delivery rides the CDN and caches with the health/drain/affinity machinery of load balancers ([[How would you explain Health checks]]), and the interview close names the next bottlenecks: feed ranking service, recommendation, and multi-region placement of both CDN and shards.

> [!warning] Do not put media bytes in the database
> Storing photos as BLOBs in the metadata DB couples the two scaling models: terabytes of cache-hostile bytes poison a row store that should hold tens of GB of hot metadata. The separation — blob storage plus CDN for bytes, sharded relational metadata for pointers — is the load-bearing decision of this design.

> [!tip] Interview answer
> I separate media from metadata: photos to blob storage with async renditions behind a CDN, sharded relational metadata for users/photos/follows, and a hybrid feed — fan-out-on-write into cached feed lists for normal users, merge-at-read for celebrities. Eventual consistency for social signals, strong for identity; bottlenecks to name next are ranking and multi-region.
