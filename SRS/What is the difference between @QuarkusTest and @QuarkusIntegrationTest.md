<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# What is the difference between @QuarkusTest and @QuarkusIntegrationTest

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: @QuarkusTest boots the app in the same JVM with augmentation artifacts, supports @InjectMock/CDI, test profile %test; @QuarkusIntegrationTest runs the packaged artifact (jar/native/container) over HTTP, no CDI injection, no mock beans; different failure feedback.
