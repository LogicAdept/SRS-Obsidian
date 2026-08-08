# SRS

`<!-- reps, priority -->` → one line of `#tags` (contains `#SRS/card`) → Markdown. No dates in meta.

- `reps`: integer ≥ 0 — number of repetitions (how exactly to count: successes only, all attempts, etc. — vault rule).
- `priority`: number (integer or decimal) — recalculated after each repetition; used to rank the queue (sorting direction — vault convention, e.g. higher `priority` = higher in the list).

```
<!--
reps: 0
priority: 0
-->
#Topic #SRS/cardAdd

...

```

**D2:** fenced `d2` block. **Layout algorithm** (`dagre` / `elk` / `tala`) — only in the D2 plugin settings or in `.obsidian/plugins/d2-obsidian/data.json` (`layoutEngine`), not in the diagram text; `tala` is configured in the vault. In the source — `direction`, edges, `width`/`height` of nodes. `d2-full-width.css` snippet (enabled in `appearance.json`): SVG spans the full column width, centered.