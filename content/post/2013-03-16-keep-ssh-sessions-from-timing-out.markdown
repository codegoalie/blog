---
layout: post
title: "Keep ssh sessions from timing out"
date: 2010-05-20
comments: true
categories: 
  - HowTo
  - Self-Reference
---

The [Ubuntu Blog]('http://embraceubuntu.com') has a nice lil' article
about [keeping SSH sessions alive]('http://embraceubuntu.com/2006/02/03/keeping-ssh-sessions-alive/')
It basically boils down to editing your `/etc/ssh/ssh_config` file and
adding the following:

    # /etc/ssh/ssh_config

    ServerAliveInterval 5

The number is the number of seconds to send the small keep alive which
keeps the connection open. Ubuntu Blog suggests changing it from 5 to
240 or 300 (4 or 5 minutes).

-- Chris
