+++
date = "2021-06-23T06:21:51-04:00"
title = "Web Scraping 2.0"
categories = ["Thoughts"]
draft = false
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

Instead of an either/or approach, a hybrid approach can be used by leveraging
browser automation _and_ API requests to quickly and reliably get the data we
need. Specifically, executing JS `fetch` requests using browser automation tools
(almost all allow arbitrary JS execution in the current "page"). Parse this
request back into the native automation language (typically JSON string returned
from JS). Bam! You have a pseudo API!

I've been very successful in pulling large amounts of data from an actively
scraper resistant environment using this approach. One of the really nice things
is that authentication/authorization for the private API requests is handled
virtually automatically by the browser through cookies.


Here's a rough outline of the entire process:

1. Manually go through the web application performing the actions intended to be
   automated while watching the network dev tools tab.
1. Note any requests of interest.
1. Generalize those requests and reverse engineer a subset of the API.
1. Begin automation.
1. Automate authentication, if necessary (Type creds into login form).
1. Evaluate JS on the page to execute the AJAX/XHR/private API requests.
1. Parse the returned string into datatypes in your native automation language.
1. ???
1. Profit!!?

My intuition leads me to believe there are some common patterns here which may
be surfaceable in a library, but my experience isn't quite to the point where I
feel confident providing the right abstractions. But, stay tuned and we'll see
how this idea unfolds.

Let me know how your experience scraping data from JS heavy web apps goes! I'd
love to know if this works for you or if this ends up being more hassle than
it's worth.

Happy scraping!
