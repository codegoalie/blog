---
layout: post
title: "Android Development: first impressions"
date: 2013-11-08
comments: true
categories: 
  - Android
---

As a web application developer working in a company full of mobile app
developers with a mobile focus and as a full time Android user, there's a
natural gravity in my universe toward mobile apps and the power of the app plus
server backend paradigm. Naturally, I wanted to build my own app and really see
what it is like on the other side of the API.

{% img left /images/android_first/car_icon.webp 150 150 Car Payment Calculaor %}
As with any new platform, language or environment, I read up extensively on the
Android ecosystem, poured over countless resources on design princiles and best
practices--NOT. I jumped right in. Since I was shopping for a new car at the
time, I whipped up a quick and dirty [Car Payment
Calculator][6].  I mostly wanted to see the whole process of building an app
and deploying it to the Anroid market. I must say the process is extremely
simple and straightforward. However, the car payment app doesn't really do
anything...
<br/>

<!-- more -->

A few form fields, a button and some quick math. No networking, no
server-side, no authorization, no fun. So, I set out on my second app: a push
notification service; something like [Boxcar][7] or [Notify My Android][9]. As
an Android user with a tablet and a phone, it's really annoying to get all my
notifications twice. I could  also scratch my own itch with some home
automation notifications as well as external services. But most importantly, I
knew this was something that I could actually build. This post isn't about
Push Something (that will come later), so enough about that.

I followed the [Google+ Sign-in for Android tutorial][8] and then the [GCM
setup tutorial][5] and finally a great [ListView tutorial][4]. Now I know that
each of these tutorials are meant to get you started and intentionally limit
the scope to only the topic at hand, but I must admit the app I ended up with,
while functional, seemed like a giant pile of spaghetti. I wasn't sure why
certain pieces of code went where, what purpose different arguments provided
to many methods (is it the class context variable, `getApplicationContext()`,
or am I passing the Activity with `this`?). And even at two activities,
debugging was becoming a game of pick a file and scroll, scroll, scroll looking
for the correct group of statements.

{% img right /images/android_first/uh_oh_android.jpg 400 200 Uh Oh Android %}
Now, I am not complaining or blaming the tutorials here. This is exactly what my
beloved Rails community does to new develoeprs as well. Dump all business logic
into the controller. No No. Move it into the model. NO NO. Service objects or
concerns and so on. Having been through that process and been at many stages
simultaneously, I am familiar and comfortable with the evolution of a Rails app.
However, being new to Android, I must admit I felt a bit lost and even
considered the possibility that Android apps were forever doomed to be a mess
of deeply nested ifs and try/catch blocks, 200+ character lines of code and
methods with a staggaring list of arguments.

Thankfully, I am the only developer on my little side project and I had to take
a break from Android land to do a little catchup work on the server side. As a
budding Rails app itself, I found myself being able to see further ahead than
ever before in my Rails code and allow myself the luxury of writing code which
doesn't make large design decisions too soon. Through experience, I am building
a solid and extensible base on which to build the rest of the app. Whoopty doo.
That's my job 5 days a week. Then I thought, why not be able to utilize some
basic OOP principles in my Java code too? These tutorials were (as most are) a
starting point; a launch pad to get the juices flowing and enable the reader
to build something truly awesome.

And that bings me to where I am at today, not rebuilding but refactoring. In the
same way I would enfore single responsibility and avoid "just throw that code
anywhere" in my Ruby code, I should do so in Java code as well. When I sat down
to write this post, I meant to document some frustration with my first Android
experiences and document my plan moving forward. But after getting this far in,
I think I'm seeing something else and one of the reasons I started
loving programming to begin with: there are always other ways to acheive the
desired results. [Give 10 developers the same requirements][3] and you'll get
_at least_ 10 different programs. Some good, some not as good. And that is the
reality of software development. It's easy to blame the language, or the
documentation, or the framework for your bad code, but at the end of the day
it's ___YOUR___ code. Own it. Be proud of it. Don't let language or framework
limitations bring down your work. You can be as awesome as you choose to be.
So don't settle for 'it works'; rest when 'it's aweosme!' Your future self
with thank your current self; instead of swearing at him. ;)  

[{% img /images/android_first/The-Time-to-Be-Awesome-is-Now-Kid-President1.jpg %}][1]

[1]: http://www.youtube.com/watch?v=l-gQLqv9f4o
[2]:
[3]: http://exercism.io/
[4]: http://www.vogella.com/articles/AndroidListView/article.html
[5]: http://developer.android.com/google/gcm/gs.html
[6]: https://play.google.com/store/apps/details?id=com.chrismar035.carpaymentcalculator
[7]: http://boxcar.io
[8]: https://developers.google.com/+/mobile/android/sign-in
[9]: http://www.notifymyandroid.com
