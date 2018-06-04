+++
date = "2018-05-11T11:24:15-04:00"
title = "Implementing filters in golang with GoBuffalo"
categories = ["golang", "Buffalo"]
+++

Filtering in web app index pages allows users to specify multiple values and
reduce a large set of records eliminating those that don't match the criteria.
Think AirB&B. I want a place with a pool and a kitchen which is in Orlando between
$250 and $300 per night. Ideally, you'd get only the places that match that criteria.

Today, we're going to discuss implementing such a feature. I chose to dicuss this today because
I just implemented something like this, I've visited code bases which also implemented this but not
very elegantly, and also because the solution I ended up with was more elegant that I was initially
expecting.

<!-- more -->

## Data model

In order to filter records, we've gotta have something to filter. For our purposes, we'll keep with the
AirB&B theme and filter `places` based on some criteria. 

> Note: I don't know anything about the internals of AirB&B. This is probably nothing like their setup.
> This post is meant to show a passable solution for a medium sized data set with average volume.

Here's the `places` struct definition:

<script src="https://gist.github.com/codegoalie/8837af00f725523b6ade8fe290338103.js"></script>
