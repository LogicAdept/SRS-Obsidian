<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

After a successful POST, dumps return a redirect view name so a refresh does not resubmit the form:

```java
if (result.hasErrors()) {
    return "todo";
}
model.clear();
return "redirect:list-todos";
```

`redirect:` is handled as a redirect (HTTP 302). Flash attributes (`RedirectAttributes`) carry a one-hop message.

> [!warning] Unverified traps from the dump
> - forward: stays in the same request; redirect: is a new GET.
> - Whether the path is relative to the servlet mapping depends on the prefix (redirect:/ vs redirect:).
