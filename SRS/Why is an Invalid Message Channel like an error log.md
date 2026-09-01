<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pattern notes compare the Invalid Message Channel to an error log for messaging. When application code hits an error, you log it. When message processing goes wrong, you put the message on the invalid channel so it is out of the working flow but still visible.

If anyone browsing the channel would not see why the message is invalid, the receiver should also log an error with more details. Ignoring the channel is described as about as useful as ignoring an error log: the messages mean integration is broken and need analysis, ideally automated, otherwise an operator process that alerts when the channel is not empty.
> [!warning] Unverified traps from the dump
> - Parking without a reason log hides the diagnosis when the payload alone looks fine.
> - Some reading notes still dump both processing errors and application errors onto the same invalid channel unless Service Activator or Messaging Gateway splits them.
