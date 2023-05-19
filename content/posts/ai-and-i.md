+++
date = "2023-05-15T19:59:01-04:00"
title = "AI and I, or You're Holding That Wrong"
categories = ["large-language-models"]
draft = false
+++

How can a tool that is indescernably wrong be anything more than a toy?

<!--more-->

You're holding that wrong. A month or so ago, I would have been the first to
laugh you off if you started talking to me about [ChatGPT](1) being an
experience like the first time you programmed or "saw the internet." It can't
even answer basic questions like those I ask my smart speaker everyday? (That's
hyperbole. I don't speak to me smart speaker nearly everyday.) Also, it lies to
you; like to your face lies to you. What even is this? A fancy [Markov chain](2)?

Well, yes, actually it is. Then I heard [Simon Willison](3) on [The
Changelog](4) and I finally got the mental model. 

> A calculator for words

-- [Simon Willison](5)

What makes these seem so terrible at first glance is the interface. Imagine if a
calculator has a single text prompt as an interface. No buttons. "Tell me the
calculation you desire." OK, so you as it to do your taxes. Unquestionably, a
calculator can't do that. But if that's your expectation, you're terribly
disappointed and go back to carrying the one with paper and pencil.

A calculator does not know your intentions or your context. It can't answer even
slightly complex questions. But, if you know how to wield it, it's incredibly
useful. It can __help__ you do your taxes and in record time*. In fact, all the
accountants that never learned to use a calculator are unemployed; replaced by
those that did.

These new LLMs are terribly persuasive. We've become used to a person being at
the other end of written words. Text messages, emails, social media posts, news
articles. A vast majority of the content we consume is written words. We've been
conditioned to assume there's a person at the other end. LLMs flip that
assumption on its head. Despite stringing together the words to be quite
convincing to the contrary, it has no feeling. It fact, it doesn't even know
what it's saying. 

Briefly, (if you already know technical details about LLMs, save yourself
from getting mad at me and skip this paragraph) LLMs are a next word/paragraph
predictor. Give some input words or sentences, it can guess, statistically which
word or sentence should come next. There's also randomness built in so you don't
get the same output twice. That's it. It's funny only because most text is also
funny in that context. It's bad at facts because you can't give random answers
_and_ be correct all the time.

So, it can't be right and it doesn't know what it's saying. How do I think about
this? What is it good at? LLMs are really good at creating a bunch of useful
words. They aren't great out of the box. You can't copy/paste straight from
ChatGPT into your homework and call it a day. But it can give you a list of
terrible ideas for something with a few gems sprinkled in. It can generate a
first draft for you.

# How to think about all this? 

First, it's not the be all, end all. It's not a silver bullet. But, it can help.
It's a starting point. It's a some, or most, of the way there. It's an intern or
beginner needing correction. It saves keystrokes. It's a first draft. It won't
replace you. Someone who uses it will.

# How I have used it to date?

I'm just scratching the surface on all of this and things are moving at an
extremely fast pace. I don't claim to be an expert but here are some examples of
ways that I've found LLMs useful.

First and most significantly, [Github Copilot](6). If you take nothing away from this post,
start using Copilot (or one of the open-source alternatives) today. Get it
integrated into your editor. The neovim integration is particularly slick. When
you pause typing, some low-lighted text will appear after your cursor. It is
suggested code from Copilot. It's especially good at handling errors or filling
small utility functions, and filling in function arguments. By accepting the
suggestion, you can save a ton of time and frustration from typos. However, it's
not always syntactically or logically correct. __You must double check its
work.__ But even so, it's a game changer for me, constantly, all day long.

Next, generating ideas. But (another gem from Simon) is to ask for tens of
ideas; like 30 - 40. Most will be useless, but there will be a few gems in there.
OR, more likely there will be a few that spur an actual good idea.

Then, I've used LLMs to help draft technical prompts. It's writing that I don't
really need to be personal or "in my voice." I really just needed some test. In
fact, the LLM added some context and details that I wouldn't have thought to
add.

Help wriring small scripts or programs; especially using an API or package I'm
not familiar with or use that often. The other day, I needed to read a CSV file,
use it to fetch some related data, generate some SQL queries and write them to
a different file. I don't work with files day to day nor CSV, but I could
quickly get a scaffold back from the LLM and fill in the actual "business logic"
bits.

How have you been using LLMs? 

One last note, I didn't use any help with this post. :)

-- Chris

* when compared to those not using a calculator


[1]: https://openai.com/product/chatgpt
[2]: https://en.wikipedia.org/wiki/Markov_chain
[3]: https://simonwillison.net/
[4]: https://changelog.com/podcast/534
[5]: https://simonwillison.net/2023/Apr/2/calculator-for-words/
[6]: https://github.com/features/copilot
