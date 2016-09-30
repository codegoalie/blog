---
categories:
- How-To
comments: true
date: 2010-06-25
layout: post
title: Trick out your Vim
---

Today, I'm going to add some plugins and scripts to make better use of Vim. I have not started this project and I will be updating this post throughout the day with my finds and experiences.

I generally use Vim to code web applications. My site at work run on PHP and at home I'm working with Ruby on Rails. So, I'll be looking for something to specifically help with that, but who knows what I'll find.

<!--more-->
# .vimrc

.vimrc is a file in your home directory. It contains a script which runs each time you start Vim. You can setup your configurations, preferences and plugins in here. The .vimrc is the starting point for fine tuning your Vim to exactly how you want it. If you are a beginner, I would recommend finding some more advanced users' .vimrc's and, at least, check them out, if not start using them for yourself. I started with <a href="http://blog.infinitered.com/entries/show/9">Todd Werth's .vimrc file</a>. He keeps his in a separate folder and uses a symlink to put them in his home folder. I strongly recommend this as well. You can automatically sync your .vimrc (or any other files) across computers with Dropbox. See how in my post on how to <a href='http://chrismar035.com/2010/06/25/use-dropbox-to-keep-your-preferences-across-computers/'>Use Dropbox to keep your preferences across Computers</a>.

Here are some useful lines to start you out:

    " Set tabs to 2 sapces
    set softtabstop=2
    set shiftwidth=2
    set tabstop=2
    set expandtab

    " Move your backup and .swp files out of the directory of the file (Helpful to keep from adding them to a repo)
    set backup
    set backupdir=~/backup
    set dir=~/swap

    " Highlight the current line
    set cursorline

    " Keyboard shortcuts (Mappings)
    c> " Use mat Insert Mode (instead of Escape)
    imap => => " Hit => to insert a "rocket" in insert mode

    " Wildmenu - show a tab completion matches list
    set wildmenu
    set wildmode=list:longest,full

Again, search the google machine and checkout github for more samples and if you find anything cool, let me know in the comments.

<h1>Plugins</h1>
<h3>Autoclose</h3>
<p>This first plugin automatically closes quotes, parenthesis, brackets, etc. for you. If you type a single quote, another single quote is added after the cursor. You can type an end paren to move the cursor after the autoclosed characters. This is helpful after nested autocloses. For instance, in PHP, I often find myself passing array values to a function:
<code>run_trail($locmotives['lionel|'])</code>
This pipe in the above example is the cursor position after the last l in lionel. I can simply hit ) and the cursor will jump out of the single quote, square bracket AND end paren. Simple.</p>
<p>Autoclose is developed by Karl Guertin and can be found at <a href='http://www.vim.org/scripts/script.php?script_id=1849'>http://www.vim.org/scripts/script.php?script_id=1849</a></p>

***Update 3/16/2013***

>  Check out [my public vim configs repo](https://github.com/chrismar035/vim_configs) for more info!

See ya Soon!

-- Chris
