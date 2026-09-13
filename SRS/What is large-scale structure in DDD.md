<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is large-scale structure in DDD?

> [!abstract] Short answer
> Large-scale structure is DDD's strategic toolbox for organizing the whole system once bounded contexts multiply: evolving order, system metaphor, responsibility layers, knowledge level, and pluggable component framework. Unlike bounded contexts, none of these is mandatory - they are patterns for imposing just enough system-wide shape that teams can navigate, and the discipline is to adopt them late and lightly, only when structure actually emerges.

## The five patterns

Evolving order is the meta-rule: let a system-wide structure become visible in what was built, then formalize it - do not legislate one up front. System metaphor is a concrete, shared story for the architecture ("the system is a warehouse with departments") that orients newcomers faster than a formal description, at the risk of overstaying its accuracy. Responsibility layers stack the contexts into tiers where each layer depends on those beneath it - an operational layer running today's business, a decision-support layer learning from it, a policy layer constraining both - so a change's blast radius reads off the stack. Knowledge level separates the model into a level that describes what kinds of things exist and a level of the things themselves - configuration-as-model, the pattern behind schema and rule engines. Pluggable component framework fixes an interface contract so implementations slot in without touching the core - the mature endgame of a stable kernel plus published interfaces.

```d2
direction: down
policy: "Policy layer\nconstraints, strategy rules" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
decision: "Decision-support layer\nanalysis, projections" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
ops: "Operational layer\ntoday's transactions" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
policy -> decision: "refines"
decision -> ops: "informs"
```

**Fig. 1.** Responsibility layers, the most usable of the five: each tier constrains or informs the one below, and a context's layer assignment tells you what kind of change it absorbs.

## When structure helps and when it suffocates

The tools answer a real problem: with ten-plus contexts, per-context discipline does not stop the system from feeling shapeless - nobody knows where a new feature belongs, and integration decisions are rediscovered per pair. A named structure fixes navigation and makes "where does this go" a lookup instead of a debate. The cost is real too: a premature structure is speculative generality with a committee attached - contexts contort to fit tiers that the business does not actually have, and refactoring across the imposed shape gets politically expensive. The middle path is evolving order plus periodic formalization: every few quarters, look at what the contexts already agree on and name only that. This is the top of DDD's strategic stack - beneath it sit per-context modeling ([[What is a bounded context and how do you identify one]]) and the pairwise contracts of [[What is context mapping in DDD]]; large-scale structure is what you reach for when those two are stable but the whole is still illegible. The founding question it answers is the same one [[What is domain driven design]] poses at scale: does the code's shape still mirror the business's shape?

> [!warning] Structure is a loan, not a gift
> Every imposed structure taxes every later change that crosses it - and the tax is paid in coordination, not code. The failure signature: a "responsibility layer" meeting where teams argue tier assignments for two sprints, or a metaphor that survives only in slide decks while the code says otherwise. If a structure cannot be stated in one sentence a new developer correctly applies, it is overhead; keep the model free until the pattern announces itself in the existing code.

> [!tip] Interview answer
> Large-scale structure is DDD's system-wide organization kit: evolving order, system metaphor, responsibility layers, knowledge level, pluggable component framework. Use it when bounded contexts multiply and navigation breaks down - and adopt it late, naming structure that already emerged rather than legislating it upfront. Its purpose is orientation: where things belong and how the parts relate, without freezing the model.

