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
tracks animals kept in a zoo. As we're mostly concerned with the authentication
part of the API, we'll only discuss three endpoints. First we have the create
token endpoint which will take our username and password and return a token.


```
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Accept: application/json
Cache-Control: no-cache

username=ned&password=$up3r$3kr3t

Response body:
{
  "access_token": "1e4kNnq0TlV6ySzDw3jY4A",
  "token_type": "BEARER",
  "refresh_token": "jncYU5a8sHZAv9PlTgxw4g",
  "refresh_expires_in": "2592000",
  "expires_in": "900"
}
```

Secondly, we have a refresh token endpoint which will take our refresh token and
return a new token for us. This will allow our client to use the API for a
longer session without requiring the user to reenter then credentials or having
very long lived tokens.

```
POST /refresh HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Accept: application/json
Cache-Control: no-cache

refresh_token=jncYU5a8sHZAv9PlTgxw4g

Response body:
{
  "access_token": "-ZK5mLCz4EtnJdjeozKPCg",
  "token_type": "BEARER",
  "refresh_token": "e6uG3-pVuceQfn4DfUwomw",
  "refresh_expires_in": "2592000",
  "expires_in": "900"
}

```

Lastly, we have the only non-auth related endpoint we will talk about. This
endpoint is a get which will return the current user's profile. In our small
API, that only includes their username.

```
GET /user HTTP/1.1
Accept: application/json
Authorization: BEARER -ZK5mLCz4EtnJdjeozKPCg

Response body:
{
  "username": "ned",
  "full_name": "Ned Plimpton",
  "occupation": "Airplane Pilot"
}

```

You might call this cheating, but by POSTing to the /user endpoint, we can
change our user's attributes. For security reasons, our API does not allow
changing your username.

```
POST /user HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Accept: application/json
Authorization: BEARER -ZK5mLCz4EtnJdjeozKPCg

full_name=Kingsley%20Zissou&occupation=Boom%20Operator

Response body:
{
  "username": "ned",
  "full_name": "Kingsley Zissou",
  "occupation": "Boom Operator"
}

```

When the tokens or credentials provided to any of these endpoints are invalid,
the API returns a 406 status code. 

# Client Interface

When designing any interface, I try to put myself in the shoes of the consumer
and define the idea usage before thinking about the internal implementation.
Ideally, I'd like to give my username and password to the class and then not
think about authentication anymore. 

```
client = MyApiClient.new(username, password)
client.user #=> <User username: "ned", full_name: "Ned Plimpton", occupation: "Airplane Pilot">
```

Our client should be initialized with username and password and then
automatically manage tokens for us. As the consumer of the client, we need not
be concerned with the implementation details of the API's authentication.

# Implementation

Separating api usage from API implementation details

Exercises:
  - Only retrying on a 406, not any server error
  - More than one retry
  - Refresh token to get new tokens without username/password
