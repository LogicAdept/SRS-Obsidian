<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: RequestCache stores a SavedRequest (URL + method + params) from before login. After success, RequestCacheAwareFilter replays it so you return to /checkout, not always /.
> [!warning] Unverified traps from the dump
> - STATELESS APIs should use NullRequestCache. Replaying a POST with a CSRF token from the old session is a dump footgun.
