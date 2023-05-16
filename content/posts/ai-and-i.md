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
even answer basic questions like those I ask my smart speaker everyday? (Thet's
hyperbole. I don't speak to me smart speaker nearly everday.) Also, it lies to
you; like to your face lies to you. What even is this? A fanct [Markov chain](2)?

Well, yes, actually it is. Then I heard [Simon Willison](3) on [The
Changelog](4) and I finally got the mental model. 

> A calculator for words

-- [Simon Willison](5)

What makes these seem so terrible at first glance is the interface. Imagine if a
calculator has a single text prompt as an interface. No buttons. "Tell me the
calculation you desire." Ok, so you as it to do your taxes. Unquestionably, a
calculator can't do that. But if that's your expectation, you're terribly
disappointed and go back to carrying the one with paper and pencil.

A calculator does not know your intentions or your context. It can't answer even
slightly complex questions. But, if you know how to weild it, it's incredibly
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

In a nutshell, (if you already know technical details about LLMs, save yourself
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

# How to think about this? 

- It's not the be all, end all.
- It's a starting point.
- It's a most of the way there.
- It's an intern or beginner needing correction.
- It saves keystrokes.
- It's a first draft.
- It won't replace you. Someone who uses this will. Period.

# How I have used it to date

- Ideas
- Writing a technical prompt
- Write scripts or code snippets for APIs I don't use often
- Copilot

* when compared to those not using a calculator


[3]: https://simonwillison.net/
[4]: https://changelog.com/podcast/534
[5]: https://simonwillison.net/2023/Apr/2/calculator-for-words/
