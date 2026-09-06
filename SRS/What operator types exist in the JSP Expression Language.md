<!--
reps: 0
priority: 0
-->
#Java/JSP/EL #SRS

# What operator types exist in the JSP Expression Language?

> [!abstract] Short answer
> **Jakarta EL 6.0 (what Pages 4.0 runs) groups operators as: property/method (`.` / `[]`), arithmetic, string concat (`+=`), relational, logical, `empty`, ternary (`?:`), assignment (`=`), semicolon (`;`), parentheses, and lambda (`->`).** Many have **word twins** (`div`, `eq`, `and`, …) so XML pages need not write `<`. Functions `prefix:name()` are **not** operators; they bind tighter than `?:`. Language: [[What do you know about the JSP Expression Language]].

## Categories, then precedence

These are **eval-expression** operators inside `${…}` / `#{…}`. Invalid syntax is a **translation error**. `null` arithmetic often becomes **`(Long) 0`**.

| Kind | Operators |
| --- | --- |
| **Property / method** | `.` `[]` — `a.b` ≡ `a["b"]`; `a.m(args)` ≡ `a["m"](args)`. EL **6.0**: arrays also have **`.length`**. |
| **Arithmetic** | `+` `-` `*` `/` `div` `%` `mod`, unary `-` |
| **Concat** | `+=` (coerce both to **String**, glue) — **not** Java `+=` |
| **Relational** | `==` `eq` `!=` `ne` `<` `lt` `>` `gt` `<=` `le` `>=` `ge` |
| **Logical** | `&&` `and`, `\|\|` `or`, `!` `not` — **short-circuit** |
| **Empty** | prefix **`empty`** — `true` for `null`, `""`, empty array / `Map` / `Collection` |
| **Conditional** | `A ? B : C` |
| **Assignment** | `A = B` — `A` must be an **lvalue**; a JSP container may set/create **page-scope** attributes |
| **Sequence** | `A ; B` — evaluate `A`, discard, return `B` |
| **Grouping** | `( )` |
| **Lambda** | `->` (right-associative; above `=` / `;`) |

**Precedence** (high → low, mostly left-to-right; `?:`, `=`, and `->` are right-assoc): `[]` `.` → `( )` → unary `-` `not` `!` `empty` → `*` `/` `div` `%` `mod` → binary `+` `-` → `+=` → relations → `==` `eq` … → `&&` `and` → `or` → `?:` → `->` → `=` → `;`.

**Word forms** exist so JSP **documents** need not put `<` in XML. Those words plus `true` `false` `null` and **`instanceof`** are **reserved** (`instanceof` is **not** an operator yet). Do not use them as identifiers.

**Not this table.** TLD **functions** (`fn:length`). **Collection pipelines** (`filter`, `map`, …) are **method calls** on streams (EL Ch. **2**), “strictly speaking not part of the language.” Set/list/map **literals** `{1,2}` `[1,2]` `{a:1}` are **construction**, not operators. Nested `${item[${i}]}` is **illegal**. Disable EL: [[How do you disable Expression Language in JSP]]. Tests in tags: [[How would you explain JSTL the JSP Standard Tag Library]]. Names: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]].

```d2
direction: down
acc: "[] .  then unary  then * /  then +  then +=" {
  width: 320
  height: 40
  style.fill: "#e3f2fd"
}
rel: "relations  then ==  then and  then or" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
tail: "?:  ->  =  ;" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
acc -> rel
rel -> tail
```

**Fig. 1.** Tightest: **property access**. Loosest: **`;`**.

```jsp
<%-- Conceptual — operator kinds --%>
<p>${cart.items[0].name}</p>
<p>${qty * price + tax}</p>
<p>${first += ' ' += last}</p>
<p>${empty param.q or param.q eq 'all'}</p>
<p>${n gt 0 ? n : 0}</p>
```

**Listing 1.** `.`/`[]`, arithmetic, `+=`, `empty`/`or`/`eq`, ternary. In XML syntax prefer `gt` over `>`.

```jsp
<%-- Conceptual — word twins and grouping --%>
<c:if test="${(a lt b) and not empty list}">ok</c:if>
```

**Listing 2.** `lt` / `and` / `not` / `empty`. `${c?b:f()}` is **illegal** (`b:f` parses as a **qualified function**); write `${c?b:(f())}`.

> [!warning] `+` does not concat; `empty` is not Java `== null`
> `${'a'+'b'}` is **arithmetic**, not `"ab"` — use **`+=`**. `${empty x}` is true for **empty collections**, not only `null`. `${a < b}` in a **JSP document** can break XML; use **`lt`**. If only one side of `==` / `eq` is `null`, the result is **false**. Do not name a bean `empty`, `eq`, or `div`.

> [!tip] Interview answer
> EL operators cover property access with dot and brackets, arithmetic with div and mod aliases, string concat with plus-equals, relational and logical operators with word forms for XML, plus empty, ternary, assignment, semicolon, and lambda arrow. Plus is numeric, not concat. Empty is true for null, empty string, and empty collections. I use lt and eq in JSP documents so I do not put raw less-than in XML.
