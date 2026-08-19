<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Model 1: a request hits a servlet or JSP that does routing, business logic, validation, and rendering. Easy for small apps; logic is duplicated and mixed with the view in larger ones.

Model 2 is MVC. The controller handles the request, puts data (often a JavaBean/POJO) on the request, chooses the view, and the view only renders.

Model 2 Front Controller is Model 2 plus a single entry servlet — Spring MVC’s `DispatcherServlet`.

> [!warning] Unverified traps from the dump
> - Model 1 is not Spring-specific; interviewers use it to contrast JSP-centric apps with Spring MVC.
