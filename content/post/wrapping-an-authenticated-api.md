+++
date = "2016-04-18T15:01:13-04:00"
title = "Wrapping an Authenticated HTTP API"
categories = ["Ruby HowTo"]
+++

- API usage
  - Authenticate and get token and expiration
  - Auth token for requests
  - 406 when token expires

Our client should:
- be initialized with username password
- automatically manage tokens for us

Client public API

`client.profile` - get own profile

Fetching the token
Performing the authenticated request
retrying on failure

Separating api usage from API implementation details


Exercises:
  - Only retrying on a 406, not any server error
  - More than one retry
  - Refresh token to get new tokens without username/password
