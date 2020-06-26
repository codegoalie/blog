---
categories:
- How-To
comments: true
date: 2010-06-25
layout: post
title: Use Dropbox to keep your preferences across Computers
---

Sometimes it can be kind of painful to discover a cool new setting or mode for on of your favorite programs. For instance, I use <a href='www.floodgap.com/software/ttytter/'>TTYtter</a>, a terminal based Twitter client. A few weeks into using it, I discovered it had ReadLine support for tab auto-completion of @usernames, in-line editing of posts and command history (up key). Awesome right? I know. Except, now I need to change my .ttytterrc file on my laptop, home computer, work computer, everywhere. Also, how do I get it there? USB drive, e-mail to myself, browse the network, etc. Being geeks, we don't want to go through all that. 

<!--more-->

Then I discovered <a href="https://db.tt/YnlXA7Ix">Dropbox</a> (that link is a referral link, <a href="http://dropbox.com">here's the regular homepage</a>). Not only is Dropbox a free 2GB of cloud storage for backing up your much needed files, but the really cool thing about Dropbox is that it <strong>automatically detects when files change and syncs them across all of your computers</strong>. Think about configuration files and read that again. Discover a new mode in any program with a config file and BAM! every computer you use has that mode enabled. The sync works in all directions so it doesn't matter which computer you make the change on, every computer gets it. Seems perfect, right?

If you're new to Dropbox, check out [this post on Cloudwards](https://www.cloudwards.net/how-to-share-files-on-dropbox/) on getting setup.

Here's how it all works. When you install the Dropox client software on your computer, it will create a Dropbox folder with all your stuff in it. Add, delete or edit any file in this folder and Dropbox will sync it up to their servers, plus download the changes to any other computer running the Dropbox client with your account. It's kind of cool to have your desktop and laptop running next to each other and watch them download the changes instantly. 

Back to business, I know what you are thinking, "All these files are in one Dropbox folder (and subfolders). My config file needs to be in my home directory. I still have to copy from my Dropbox to my home." Well, let's let the computer do the copying. Actually, let's not even waste time and space copying. Let's create a symlink to make the config files appear to be in your home folder but actually be stored in the Dropbox folder.

First, open a terminal, navigate to the Dropbox folder and create a new subfolder; I called mine 'configs.'

    $ cd ~/Dropbox
    $ mkdir configs
    $ cd configs

Now, let's move the config file from the home folder into the Dropbox/configs folder and navigate to the home folder.

    $ mv ~/.ttytterrc ~/Dropbox/configs/.ttytterrc
    $ cd ~/

Here's the magic. We'll create a symlink (like a shortcut in Windows) which will make it appear that the file is in your home directory, but Dropbox will still keep track of it.

    $ ln -s ~/Dropbox/configs/.ttytterrc ~/.ttytterrc

Rough Spot: If you get a file exists error, the link will not overwrite an existing file. Remove the file from where you are creating the link into (the home dir in our case).

Do this on all your computers, then you can edit the file directly from my home directory on any computer and the changes will be automatically propagated to all my other computers instantaneously. 


Here are some other ideas for this technique which I haven't tried, but might be cool.
<ul>
<li>Thunderbird Profile
<li>Media Library
<li>Flat data files
</ul>
If you have any more or try one of these, let me know in the comments!

-- Chris
