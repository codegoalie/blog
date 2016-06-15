+++
date = "2016-04-18T15:01:13-04:00"
title = "Wrapping an Authenticated HTTP API"
categories = ["Ruby HowTo"]
+++

Today, we'll look at using an authenticated third party HTTP API in Ruby in
order to use it in our application without the need to handle the underlying
authentication manually. This is a pattern I use often with authenticated third
party APIs and find that abstracting the implementation allows me to write much
cleaner application code focused on my domain instead of the API.

<!-- more -->

First, let's define our example API which we'll work against. This service
tracks animals kept in a zoo. It has three main endpoints we'll work with.
The first 


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
