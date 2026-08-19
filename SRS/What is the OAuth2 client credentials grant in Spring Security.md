<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Client credentials is machine-to-machine: no end-user. The client authenticates with client-id and client-secret at the token endpoint and receives an access token for its own scopes.

Dumps contrast it with authorization code (user present) and with the password grant (user password given to the client). Spring apps use it as an OAuth2 client calling another resource server.
> [!warning] Unverified traps from the dump
> - This grant cannot represent a user principal. Do not use it for ‘login as this person’.
