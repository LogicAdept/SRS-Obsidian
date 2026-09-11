<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# When should you not use a separate Invalid Message Channel

> [!abstract] Short answer
> Skip it for simple applications with little error processing, and whenever the extra channel's complexity outweighs the benefit of separate handling. The trade-offs are real: another channel to operate, extra storage for parked messages, and a more complicated workflow because invalid traffic is handled off the main path.

## Costs, and what "not separate" still means

The when-not-to-use guidance mirrors the when-to-use list. Operating an additional channel means provisioning, monitoring, and access control; parked messages consume storage indefinitely until drained; and the workflow grows a second path — triage consumers, reason conventions, replay procedures — that somebody has to own. In a small system with a couple of well-known senders and little error processing, those costs can exceed the value of a quarantine; folding invalid detection into the ordinary error handling may be honest enough, provided the failure still becomes visible — the pattern's core warning is that silent consumption and requeue loops are the two wrongs the channel exists to prevent ([[What happens if a receiver puts an invalid message back on the original channel]]).

Skipping a *dedicated* channel does not mean ignoring invalid traffic: products often provide a dead-letter sub-queue as the only parking place, and receivers can use it deliberately with strict reason headers — the implementation shape in [[How do you implement Invalid Message Channel when the broker only has a dead-letter sub-queue]] — at the cost of mixing broker-dead traffic, the split kept in [[What is the difference between Invalid Message Channel and Dead Letter Channel]]. Large estates also face the cost dimension: dedicated error channels across hundreds of entities multiply the operational bill, so platform teams often standardize on shared quarantine infrastructure instead.

> [!warning] "Simple app" is a trap in interviews
> The rule is not "invalid messages never happen in simple apps" — it is that the *separate channel* is not worth it. If the system still receives contract-breaking traffic, something must park or at least log it; choosing no channel must be a conscious simplification, not an omission. The positive criteria for adding one are in [[When should you use the Invalid Message Channel pattern]], and the pattern statement itself in [[What is the Invalid Message Channel pattern]].

> [!tip] Interview answer
> Don't build one when the system is small and error handling is minimal — the extra channel, its storage, and the off-main-path workflow cost more than they protect. But say what you do instead: either fold invalid handling into ordinary error processing with visibility, or use the broker's dead-letter sub-queue with disciplined reasons. Skipping the channel is never license to requeue or drop silently.
