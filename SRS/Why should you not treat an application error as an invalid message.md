<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A message can be well-formed and still fail in the domain. Example: a Command Message that tells the receiver to delete a database record that does not exist. That is an application error, not a messaging error. Moving it to the Invalid Message Channel is misleading because there is nothing wrong with the message.

The split is clearer when the receiver is a Service Activator or Messaging Gateway: errors while decoding or validating the message are invalid-message cases; errors while the application processes already-extracted data are application errors and should be handled as failed requests, not as invalid messages.
> [!warning] Unverified traps from the dump
> - Some CPI write-ups put every exception, including missing outbound auth, onto an InvalidMessages queue.
> - One dump says an invalid field value should not go to the Invalid Message Channel, while other dumps treat malformed values as exactly that pattern.
