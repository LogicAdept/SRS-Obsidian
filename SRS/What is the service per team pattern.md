<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceBoundaries #SRS

# What is the service per team pattern

> [!abstract] Short answer
> Service per team: each service is owned by exactly one team with sole responsibility for changing it, and ideally a team owns exactly one service. The pattern answers "what is the relationship between teams and services": teams of 5-9 people, codebases sized to the team's cognitive capacity, one codebase deployed as one or more services. Autonomy and loose coupling are properties of the org-architecture fit, not of the code alone.

## Mechanism: ownership as a design decision

The pattern fixes ownership as a first-class constraint on decomposition. A team owns a code base - nobody else merges changes into it - and deploys it as one or more services. The granularity rule is unusual and worth quoting precisely: aim for exactly one service per team unless there is a proven need for more. One team, one service means the team owns the full lifecycle of one business capability - build, test, deploy, operate - with zero coordination overhead on the happy path. Multiple services per team are the concession: justified when one capability genuinely splits by deployment or scaling characteristics, not to look fine-grained.

This inverts how decomposition is often done. Instead of drawing service boundaries first and assigning teams to whatever results, you let the team capacity shape the boundaries: the forces include that a team's codebase must not exceed its cognitive capacity, and that finer-grained decomposition improves the -ilities (maintainability, testability, deployability) while adding distributed-systems complexity. The equilibrium point is one capability-sized service per capable team. The decomposition patterns that propose the boundaries are [[How do you decompose an application by business capability]] and [[How do you decompose an application by subdomain]]; this pattern is the constraint that says the boundaries must also make organizational sense - each team autonomous, able to develop and deploy with minimal collaboration with other teams.

```d2
direction: right
org: "Engineering org" {style.fill: "#eceff1"}
t1: "Orders team
5-9 people" {style.fill: "#e8f5e9"}
t2: "Inventory team
5-9 people" {style.fill: "#e8f5e9"}
t3: "Delivery team
5-9 people" {style.fill: "#e8f5e9"}
s1: "Order service" {style.fill: "#e8f5e9"}
s2: "Inventory service" {style.fill: "#e8f5e9"}
s3: "Delivery service" {style.fill: "#e8f5e9"}
org -> t1
org -> t2
org -> t3
t1 -> s1: sole owner, ideally 1:1
t2 -> s2: sole owner
t3 -> s3: sole owner
s1 -> s2: API only, no shared DB
```

**Fig. 1.** Teams and services align one-to-one; cross-service arrows are contracts between teams, not shared code or shared data.

## Benefits and the acknowledged drawback

The benefits: team autonomy with minimal coordination, loosely coupled teams, and the minimum number of services that achieves both - plus long-term code ownership improving quality, because a team that will maintain its service for years has skin in the code's health. The acknowledged drawback cuts deep: teams are not necessarily aligned with end-user features, so implementing a feature that spans services requires collaboration across teams. This is the trade-off to state in an interview: ownership-aligned boundaries buy autonomy and quality at the price of cross-team feature work, which is exactly the trade-off Conway's-law thinking predicts. It also explains why this pattern belongs to the granularity conversation: if many user stories routinely touch four services owned by four teams, the decomposition - not the teams - is usually wrong.

> [!warning] Shared ownership is no ownership
> The failure mode this pattern forbids: two teams committing to one service "to move fast". Merge conflicts, conflicting priorities and regression ping-pong follow, and accountability dissolves. A second trap: one team owning ten services - cognitive overload with the same symptoms, outages from nobody remembering service number nine's quirks. If either situation exists, the boundary map needs redrawing: split the overloaded team's portfolio, merge the multiply-owned service into one owner.

> [!tip] Interview answer
> Service per team means one team owns each service end to end - ideally exactly one service, sized to the team's cognitive capacity. Ownership drives the decomposition: business capability or subdomain boundaries are adjusted until each team can build, test and deploy autonomously. I accept that cross-service features need cross-team coordination - the payoff is real autonomy and long-term code quality. Shared ownership of a service is the anti-pattern to refuse.
