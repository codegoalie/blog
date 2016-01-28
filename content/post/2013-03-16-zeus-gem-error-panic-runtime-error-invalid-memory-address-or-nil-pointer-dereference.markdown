---
categories:
- HowTo
- Self-Reference
comments: true
date: 2013-02-12
layout: post
title: 'Zeus gem error: "panic: runtime error: invalid memory address or nil pointer
  dereference"'
---

I was getting this error and the <a href="https://github.com/burke/zeus">excellent Zeus rails environment loader gem</a> was crashing making it a huge bummer to dev. 

Luckily, I found a fix in <a href="https://github.com/burke/zeus/issues/103#issuecomment-11236004">one of the open issues on the project</a>.

It was easy to fix, just run a bundle install to add the missing gems:

<pre lang='bash'>$ bundle install</pre>

Easy as that. Hope this helps someone else!

-- Chris
