<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`FlashMap` stores attributes for the **next** request after a redirect (PRG). Typical API is `RedirectAttributes.addFlashAttribute`.

```java
redirectAttributes.addFlashAttribute("message", "Save successful");
return "redirect:/result";
```

The following request reads the attribute (dumps: `@ModelAttribute("message")`) then the flash map is cleared.

> [!warning] Unverified traps from the dump
> - Flash attributes are not the same as @SessionAttributes (they survive only one redirect hop).
