+++
date = "2016-04-18T15:01:13-04:00"
title = "Wrapping an Authenticated HTTP API"
categories = ["Ruby", "How-To"]
+++

Today, we'll look at using an authenticated third party HTTP API in Ruby in
order to use it in our application without the need to handle the underlying
authentication manually. This is a pattern I use often with authenticated third
party APIs and find that abstracting the implementation allows me to write much
cleaner application code focused on my domain instead of the API.

<!-- more -->

First, let's define our example API which we'll work against. This service
is very simple in that in only allows us to authenticate and get & update our
own profile. As we're mostly concerned with the authentication part of the API,
we'll only discuss three endpoints. First we have the create token endpoint
which will take our username and password and return a token.

``` http
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

The `/token` endpoint returs two tokens for us. The access token is used to
authenticate against the other endpoints of the API. We'll use the
`Authorization` header with the token and the type. The refresh token will be
used to get new tokens when our access token expires. Using only these two tokens
we can maintain access to the API on behalf of a user without the need to store their
credentials while avoiding very long lived tokens.

We can refresh our tokens with the refresh `/endpoint`.

``` http
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
endpoint is a get which will return the current user's profile.

``` http
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

We can also update our profile by `POST`ing to that endpoint.

``` http
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
and define the ideal usage before thinking about the internal implementation.
Ideally, I'd like to give my username and password to the class and then not
think about authentication anymore. 

``` ruby
client = MyApiClient.new(username, password)
user = client.user #=> <User username: "ned", full_name: "Ned Plimpton", occupation: "Airplane Pilot">
user.full_name = 'Kingsley Zissou'
user.occupation = 'Boom Operator'
user.update
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
