<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump lists a sender putting a perfectly good message on the wrong channel as a way a receiver gets a message that makes no sense. The messaging system delivers it. The receiver on that channel expected a different type or meaning, so it cannot process the payload even though another receiver on the intended Datatype Channel could have.

The receiver treats the delivered message as invalid and moves it to the Invalid Message Channel rather than leaving it on the working channel or dropping it. The dump's rule is that validity is the receiver's expectations, not a property of the message itself.
> [!warning] Unverified traps from the dump
> - Parking on the Invalid Message Channel isolates the evidence; the repair is to send on the channel whose receivers share that contract.
> - Sharing one channel across receivers with different contracts produces the same symptom: messages that are valid for someone else look invalid here.
