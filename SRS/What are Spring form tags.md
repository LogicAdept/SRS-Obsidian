<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The Spring form tag library binds JSP fields to a command object and shows binding errors.

Dump `todo.jsp`: `<form:form method="post" commandName="todo">`, `<form:input path="desc"/>`, `<form:errors path="desc"/>`.

`commandName` / `modelAttribute` must match the model attribute used in the controller. Errors come from `BindingResult`.

> [!warning] Unverified traps from the dump
> - commandName is the older attribute; newer dumps use modelAttribute.
> - These tags are JSP-centric; Thymeleaf uses th:object / th:field instead.
