+++
date = "2021-06-23T06:21:51-04:00"
title = "Web Scraping Two Dot Oh"
categories = []
draft = true
+++

With the wide adoption of robust front-end frameworks and CSS-in-JS,
traditional methods of targeting xpath or CSS selectors for scraping data from
web pages are becoming ineffective. However, this new paradigm of front-end
development leaves a key opportunity to improve the web scraping experience.

<!--more-->

Having data that's not readily available in an API is something that I've kind
of become obsessed with over the past year or so. Even with access to
[public](https://github.com/awesomedata/awesome-public-datasets)
[datasets](https://github.com/dolthub/dolt) becoming more and more prevalant, I
still wanted access to data from websites or companies that I use but have no
interest in separating their data from their platform. So, how do you scrape a
React or Angular or other front-end framework app/site? While scraping the data
from the HTML may not be feasible or break constantly, you can use their API.
The same API the front-end uses. However, often these private APIs are resistant
to general use through opaque authentication and authorization mechanisms which
make them more work than it's worth to try and write a traditional API client.

## Why not both?

Instead of an either/or approach, we can use a hybrid approach using browser
automation _and_ API requests to quickly and reliably get the data we need.

## A little history




Additional content
