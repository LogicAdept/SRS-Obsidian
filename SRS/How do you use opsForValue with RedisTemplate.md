<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS

# How do you use opsForValue with RedisTemplate?

> [!abstract] Short answer
> Call **`redisTemplate.opsForValue()`** to get a **`ValueOperations`** view for Redis **string** commands (`SET`/`GET`/`INCR`, …). Use it for simple key→value storage with optional TTL, conditional sets, and numeric increments — sibling views (`opsForHash`, `opsForList`, …) cover other Redis types.

## ValueOperations view

`RedisTemplate` groups Redis commands into operational views. **`opsForValue()`** returns **`ValueOperations`**: Redis string (value) operations with your configured key/value serializers.

```java
@Autowired
RedisTemplate<String, User> redisTemplate;

void cacheUser(User user) {
  redisTemplate.opsForValue().set(
      "user:" + user.id(), user, Duration.ofMinutes(30));
}

User load(String id) {
  return redisTemplate.opsForValue().get("user:" + id);
}

boolean tryLock(String orderId) {
  Boolean ok = redisTemplate.opsForValue().setIfAbsent(
      "lock:order:" + orderId, "1", Duration.ofSeconds(10));
  return Boolean.TRUE.equals(ok);
}

long bumpViews() {
  Long n = redisTemplate.opsForValue().increment("page:views:home");
  return n != null ? n : 0L;
}
```

**Listing 1.** Common `ValueOperations` calls: set-with-TTL, get, set-if-absent, increment (Spring Data Redis `ValueOperations` / template views).

You can also inject the view directly (`@Resource(name = "redisTemplate") ValueOperations<…>`) so callers avoid repeating `opsForValue()`.

```d2
direction: right
tmpl: "RedisTemplate" {
  style.fill: "#e3f2fd"
}
val: "opsForValue()\nValueOperations" {
  style.fill: "#e8f5e9"
}
other: "opsForHash / List\nSet / ZSet / …" {
  style.fill: "#fff3e0"
}
cmds: "SET GET INCR\nSET NX + EX" {
  style.fill: "#f3e5f5"
}

tmpl -> val -> cmds
tmpl -> other
```

**Fig. 1.** `opsForValue` is the string/value view; other `opsFor*` views map to other Redis data structures.

## Typing and serializers

Return and argument types follow the template’s type parameters and serializers. With `RedisTemplate<String, User>` and a JSON value serializer, `get` returns `User` (or `null`). With a looser `RedisTemplate<String, Object>`, you may need casts — prefer a typed template or `StringRedisTemplate` for string payloads.

> [!warning] `setIfAbsent` is not a full distributed lock
> `setIfAbsent(key, value, Duration)` maps to Redis **SET NX** with expiry — a useful short-lived flag. It is **not** a Redisson-style lock (no fencing token, no safe unlock protocol, no reentrancy). Do not treat it as complete distributed locking.

> [!warning] Serialization still applies
> Values go through the template’s **value serializer**. Default JDK serialization is unsafe for untrusted data; configure JSON (or another format) explicitly — see [[Why should you avoid JdkSerializationRedisSerializer]].

> [!tip] Interview answer
> `opsForValue()` gives the Redis string API on `RedisTemplate`: set/get, optional TTL, set-if-absent, and increment. Other Redis types use other views like `opsForHash`. Prefer a typed template so `get` returns your domain type, and remember set-if-absent alone is only a simple NX flag, not a full lock library.

See [[How do you store a Redis value with a TTL]], [[What is RedisTemplate]], and [[What is the difference between RedisTemplate and StringRedisTemplate]].
