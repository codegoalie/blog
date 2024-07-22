+++
date = "2024-07-22T05:18:09-04:00"
title = "golibnotify 0.2.0 released!"
categories = ['Golang', 'Open Source', 'My Stuff']
draft = false
+++

[`golibnotify`](https://github.com/codegoalie/golibnotify) is 
a Go library for sending desktop notifications on Linux. It is
a wrapper around the `libnotify` library. 

There are some memory leak fixes in the latest release, `v0.2.0`.

<!--more-->

Big thank you to [Stefan van den Akker (@omhaal)](https://github.com/omhaal)
for fixing some unfreed memory in the `SimpleNotifier`. I'm not a c or cGo export
so I really appreciate it!

Be sure to update your go.mod files to `v0.2.0` and let me know if you run into
any other bugs or issues!

Happy notifying!
