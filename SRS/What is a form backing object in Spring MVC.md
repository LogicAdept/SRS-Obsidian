<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A form backing object (command object) is a POJO that collects submitted form fields. It holds data only, no business logic.

The controller exposes it on GET (often `model.addAttribute("todo", new Todo(...))`) and binds the POST onto the same type (`@Valid Todo todo, BindingResult result`). Spring form tags bind paths to that object’s properties.

> [!warning] Unverified traps from the dump
> - It is the same idea as @ModelAttribute on a parameter, under an older name.
