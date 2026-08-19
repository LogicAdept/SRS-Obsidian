<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Model` is an interface: a holder for attributes. You add data and **return a view name string**.

`ModelMap` is a Map-like implementation (dumps: extends `LinkedHashMap`) with the same role; `addAttribute` wraps `put` with a null check and returns `this` for chaining.

`ModelAndView` is an object you return: both the model data and the view name live on it (`setViewName`, `addObject`).

> [!warning] Unverified traps from the dump
> - ModelMap vs ModelAndView is already a nearby card; this dump treats all three together.
