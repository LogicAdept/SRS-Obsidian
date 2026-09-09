<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: quarkus-junit5 provides @QuarkusTest which boots the application in test profile before tests; HTTP asserted with REST Assured; @TestHTTPEndpoint targets a resource class; @InjectMock mocks CDI beans; @TestProfile or @TestResource customize the test context.
@QuarkusIntegrationTest launches the actual build artifact (JVM jar, native executable, or container image) and tests it over HTTP; mocking is not supported there.
Dev Services give the tests databases/brokers automatically; continuous testing runs tests in the background as code changes.
Tests run with profile "test" by default; quarkus.test.* properties tune behavior.
Trap: @QuarkusTest still runs in JVM mode; it does not validate native-mode behavior — use @QuarkusIntegrationTest with the native artifact for that.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
