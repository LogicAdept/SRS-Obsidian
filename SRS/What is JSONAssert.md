<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #DataFormats/JSON #SRS

# What is JSONAssert?

> [!abstract] Short answer
> **JSONAssert** (`org.skyscreamer.jsonassert.JSONAssert`) is a **logical JSON equality** library, not a Spring type. `JSONAssert.assertEquals(expected, actual, strict)` compares structure and values instead of brittle full-string equals. The boolean maps to **`JSONCompareMode.STRICT`** (`true`) or **`LENIENT`** (`false`). Spring MVC Test **requires this JAR** for `content().json(…)` and MockMvc AssertJ **`bodyJson().isLenientlyEqualTo` / `isStrictlyEqualTo`**.

## Strict vs lenient (two flags, four named modes)

`JSONCompareMode` is two independent bits: **extensible** (actual may have **extra object keys**) and **strict array order**.

| Mode | Extra object fields | Array order |
| --- | --- | --- |
| `STRICT` (`strict = true`) | fail | must match |
| `LENIENT` (`strict = false`) | allowed | ignored |
| `NON_EXTENSIBLE` | fail | ignored |
| `STRICT_ORDER` | allowed | must match |

The **boolean overload only picks STRICT or LENIENT**. Official cookbook: **object key order never matters**, even in strict mode. **Arrays cannot be “extended”**: extra or missing elements fail in **both** modes. Authors recommend defaulting **`strict = false`** so APIs can grow fields.

```java
String actual = "{id:1,name:\"Juergen\"}";
JSONAssert.assertEquals("{id:1}", actual, false); // pass (LENIENT, extra name OK)
JSONAssert.assertEquals("{id:1}", actual, true);  // fail (STRICT, extra name)

JSONAssert.assertEquals("[1,2,3,4,5]", "[5,3,2,1,4]", false); // pass
JSONAssert.assertEquals("[1,2,3]", "[1,2,3,4,5]", false);     // fail — arrays not extensible
```

**Listing 1.** Conceptual cookbook cases. Arguments may be `String`, `JSONObject`, or `JSONArray` (`org.json`). Non-strict comparison **throws `IllegalArgumentException`** (not a false pass) for mixed-type arrays or arrays-of-arrays.

## Where Spring plugs it in

MockMvc `content().json(expected)` parses both sides and asserts **lenient** similarity (needs JSONassert on the classpath). Framework **6.2**: prefer **`content().json(expected, JsonCompareMode.STRICT)`** (Spring’s two-value `org.springframework.test.json.JsonCompareMode`); **`json(String, boolean)` is deprecated**. AssertJ MockMvcTester: `bodyJson().isLenientlyEqualTo("sample/hotel-42.json")` (classpath `*.json` file or raw content). JsonPath (`jsonPath("$.name")`) is a **different** library for **one path**, not whole-document compare. How to wire MockMvc: [[How do you write a MockMvc test]], [[What is MockMvc]]. Path queries: [[How would you explain JSONPath]].

```d2
direction: down
raw: "response body String" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ja: "JSONAssert / content().json" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
mode: "STRICT vs LENIENT\n(extensible × array order)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

raw -> ja
ja -> mode
```

**Fig. 1.** Spring does not reimplement comparison. It delegates to JSONAssert (or a `JsonComparator` you supply).

> [!warning]False is not “ignore the rest of the array”
> `assertEquals(expected, actual, false)` allows **extra object fields** and **reordered arrays**. A **longer or shorter array still fails**. For “no extra fields, but array order free,” use **`NON_EXTENSIBLE`**, not the boolean.

> [!warning]Classpath, not a Spring class
> `org.skyscreamer.jsonassert` must be a test dependency or `content().json` / `bodyJson().isStrictlyEqualTo` will not run. String `equals` on minified vs pretty JSON is the brittleness this library avoids.

> [!tip] Interview answer
> **JSONAssert is skyscreamer’s JSON structural assert, used under MockMvc `content().json`.** `false` is LENIENT: extra object keys OK, array order ignored, array length still exact. `true` is STRICT: no extra keys, arrays in order. Spring 6.2 prefers `JsonCompareMode` over the boolean. JsonPath is for one field, not the whole document.
