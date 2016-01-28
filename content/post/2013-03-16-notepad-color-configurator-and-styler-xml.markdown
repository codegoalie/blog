---
layout: post
title: "Notepad++ Color Configurator and styler.xml"
date: 2010-01-08
comments: true
categories: 
  - HowTo
  - Self-Reference
---

Before I start talking about colors, let's talk font.
[Consolas](http://www.microsoft.com/downloads/details.aspx?familyid=22e69ae4-7e40-4807-8a86-b3d36fab68d3&displaylang=en).
That's all you need to know. By far the best programming font. Get it. Use it. Love it.

<!--more-->

Recently I started learning Ruby on Rails and I found
[RailsCasts](http://railscasts.com/) with a ton of Rails focused screencasts.
I believe he use [TextMate](http://macromates.com/) for mac. I hadn't really
thought much about color in my code before watching some of these screencasts.
But, it actually helps, a lot! I use Notepad++ in Windows and they have a great
styling system. You can use the in program Style Confirurator or you can
directly modify the XML style sheet.

# Style Configurator

The Style Configurator is a dialog within Notepad++ accessible through the
Settings menu. The really great thing about the Configurator is that the styles
you choose are updated live in your code. So, open up a file with a lot of code.
Then open the Configurator and move it over to another screen. If you don't have
more than one monitor, check the Transparency box in the lower right and you
will be able to see through the Configurator. The slider there sets the
Transparency level. Now you can see all of your code and pick styles for them.

Start with the very first 'language,' Global Styles. These not only include
default styles of text but many of the stuff around your code, such as line
number margin, inactive and active tab color, and the edge. The edge is great
to keep your lines of code to a certain length for printing or displaying in a
terminal. I also set the global font to Consolas. Also, be sure to set the
current line color and selected text background color.

Now you are ready to style for you language. I usu PHP mostly at work so I'll
go though that one. Hopefully, I'll be familiar with Ruby soon enough to write
a post about Ruby styles.

* QUESTION MARK - This is the style of the opening and closing php tags
  ('<?php' and '?>')
* DEFAULT - Text that doesn't match any of the other styles will be this.
* STRING - Any string enclosed with double quotes
* STRING VARIABLE - variables enclosed withing literal strings: "The Count is
  $count"
* SIMPLESTRING - These are string enclosed with single quotes. (I used a very
  similar green to STRING)
* WORD - These are the keywords of PHP. There are a bunch defined. You can also
  define some of your own in the blank box.
* NUMBER - Number literals, including array indices
* VARIABLE - Any word started with a $
* COMMENT - Text between matching multi-line comments ('/*' and '*/')
* COMMENTLINE - Text on a line after and including two forward slashes (//)
* OPERATOR - Operators (+,=,-,etc.), matched parenthesis, brackets, curly
  brackets and logical operators

# Stylers.xml

The stylers.xml file contains all the settings from the Configurator used by
Notepad++. In addition to using the Configurator, you can manually edit this
file. Or, download one from the web. The [Notepad++ 
site](http://notepad-plus.sourceforge.net/uk/download.php) has some under Theme
Files. [Joy Boner](http://joyboner.com/60-free-textmate-notepad-styler-themes/)
(read the [about page](http://joyboner.com/about/)) has 60 themes. I didn't
check any of these out, but it might be worth a shot if you really don't want
to set your own styles. 

I also put [my personal stylers.xml](http://gist.github.com/272115) as a gist
on github. Feel free to fork it.

If you have any other Notepad++ styling tips, comment below!

--Chris
