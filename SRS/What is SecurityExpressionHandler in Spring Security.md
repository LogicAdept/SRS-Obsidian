<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SecurityExpressionHandler builds the SpEL EvaluationContext for web and method security (createEvaluationContext, return object, filter object). DefaultWebSecurityExpressionHandler / DefaultMethodSecurityExpressionHandler are the dump bases.

Override it to add custom root methods or variables so @PreAuthorize can call your DSL. Register via http.authorizeRequests().expressionHandler(...) or the method-security configurer.
> [!warning] Unverified traps from the dump
> - Web and method expression handlers are different beans. Customizing only HttpSecurity does not change @PreAuthorize.
