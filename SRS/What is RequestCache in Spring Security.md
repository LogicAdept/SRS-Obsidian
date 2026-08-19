<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: RequestCache stores the SavedRequest from before login so RequestCacheAwareFilter can replay it after success (you land back on the page you wanted, not always /).
> [!warning] Unverified traps from the dump
> - HttpSessionRequestCache does nothing useful for STATELESS JWT APIs. NullRequestCache is the dump pairing with token auth.
