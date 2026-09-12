<!--
reps: 0
priority: 0
-->
#Security/Authorization #SRS

# What is the difference between RBAC and ABAC

> [!abstract] Short answer
> RBAC grants permissions **through roles**: users are assigned roles, roles carry permission sets, and the check asks "does this subject's role allow this action". ABAC decides per request from **attributes** - of the user, resource, action, and environment - evaluated by policy ("department == owner-department AND shift is active"). RBAC is simpler to administer and audit; ABAC expresses contextual rules RBAC cannot say without exploding into roles. Real systems are hybrids: role gates plus attribute conditions.

## The two decision models

```d2
direction: right
rbac: "RBAC\nuser -> roles -> permissions" { width: 300; height: 80; style.fill: "#e3f2fd" */
abac: "ABAC\npolicy(user attrs, resource attrs,\nenv attrs) -> decision" { width: 330; height: 100; style.fill: "#e8f5e9" */
```

**Fig. 1.** The indirection difference: RBAC routes through a role layer; ABAC evaluates attributes directly against policy at decision time.

- **RBAC** (role-based): the admin-defined matrix of role -> permissions. Strengths: reviewability ("who has the Approver role?"), clean onboarding, compliance mapping. Weaknesses: no context - "manager of *this* record's department" or "access during working hours from a managed device" requires either new roles per combination (role explosion) or a workaround.
- **ABAC** (attribute-based): the policy engine evaluates attributes - subject (department, clearance, employment status), resource (owner, classification, region), action, environment (time, network, device posture). Strengths: contextual, fine-grained, scales with rules not role count. Weaknesses: policies are code - harder to review, easier to get subtly wrong; "who can access X" may not have a static answer.

```java
// RBAC gate + ABAC condition - the common hybrid
@PreAuthorize("hasRole('APPROVER') and #order.department == authentication.department")
public void approve(Order order) {}
```

**Listing 1.** Spring Security method security expressing both layers: the role is the coarse gate, the attribute comparison is the contextual rule ([[What is hasPermission in Spring Security method expressions]]).

## Where each fits

- **RBAC is the backbone**: most enterprise access maps cleanly - admin, editor, reader, approver; clusters like Kubernetes RBAC, database roles, and cloud IAM role/permission bindings are all this model ([[What is the difference between authentication and authorization]] - roles only matter once identity is established).
- **ABAC is the edge layer**: ownership checks, time/place/policy conditions, multi-tenancy isolation - the rules that would multiply roles combinatorially. Zero-trust policy engines are attribute machines by design: SP 800-207's dynamic policy evaluates "client identity, application/service, and the requesting asset" - attributes all ([[What is zero trust architecture]]).
- **ReBAC** (relationship-based, "document owner can edit") is the third practical variant - relationships as the attribute source, common in document-sharing systems.

> [!warning] "ABAC replaces RBAC"
> Teams that go all-in on attributes lose the audit and onboarding simplicity roles gave them, and end up debugging policy engines like code with no test seam. The other direction is worse: role explosion - `Editor_EMEA_Night_Ops_ReadOnly` - is the smell of contextual rules being squeezed into a role matrix. The workable design uses roles for stable responsibility boundaries and attributes for the contextual remainder ([[What is the principle of least privilege]] is the goal both serve).

> [!tip] Interview answer
> RBAC decides through roles - user to role to permissions, easy to review, but static and context-blind; ABAC evaluates attributes of user, resource, and environment against policy - contextual and fine-grained, but policy-as-code with review cost. Production systems are hybrids: role gates plus attribute conditions, with relationships (ReBAC) where sharing semantics demand it.
