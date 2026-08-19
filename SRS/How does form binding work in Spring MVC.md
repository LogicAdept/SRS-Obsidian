<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Form binding maps request parameters (HTML form fields) onto a command object so you do not parse each field by hand.

`@ModelAttribute` on a **method parameter**: Spring gets or creates the named model attribute, then fills matching request parameter names onto its properties, then passes it to the handler.

`@ModelAttribute` on a **controller method**: that method runs before `@RequestMapping` handlers and adds attributes to the model. On a `@ControllerAdvice` class those attributes are global defaults for every request.

Spring MVC form tags bind page fields to the same bean.

> [!warning] Unverified traps from the dump
> - `@ModelAttribute` methods run before request-mapping methods.
> - Binding is not validation — Bean Validation / Hibernate Validator is a separate step.
