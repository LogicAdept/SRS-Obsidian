<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@SessionAttributes` is a **class-level** annotation listing model attribute names that Spring should store in the HTTP session (conversational storage) after the handler runs.

`@SessionAttribute` is a **method parameter** annotation that reads an attribute already managed in the session (often globally, not only by this controller’s `@SessionAttributes`).

Same name on `@ModelAttribute` and `@SessionAttributes` is how dumps show promoting a model attribute into the session.

> [!warning] Unverified traps from the dump
> - SessionAttributes is not the same as stuffing values into HttpSession yourself.
> - Dumps mix @SessionAttribute (singular, parameter) with @SessionAttributes (plural, type).
