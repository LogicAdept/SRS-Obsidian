<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Mocking #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

in28minutes dump:

```java
Mockito.when(surveyService.retrieveQuestion(anyString(), anyString()))
    .thenReturn(mockQuestion);
RequestBuilder requestBuilder = MockMvcRequestBuilders.get(
    "/surveys/Survey1/questions/Question1").accept(MediaType.APPLICATION_JSON);
MvcResult result = mockMvc.perform(requestBuilder).andReturn();
JSONAssert.assertEquals(expected, result.getResponse().getContentAsString(), false);
```

GFG-style: `mockMvc.perform(get("/").param("name", "Geeks")).andExpect(status().isOk()).andExpect(view().name("welcome-page"))`.

> [!warning] Unverified traps from the dump
> - strict=false JSONAssert ignores extra fields and unordered keys — easy to hide bugs.
