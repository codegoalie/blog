---
categories:
- HowTo
- Self-Reference
comments: true
date: 2011-02-15
layout: post
title: Ruby Auto-Responder for Postfix/Vmail
---

Not knowing perl, I set out to write my own script in Ruby to send auto-responses from e-mail addresses setup in a vmail folder structure. You don't need to use postfix, just have the 'new' folder where new messages are stored.

<!--more-->

I recently moved our company's e-mail server to <a href="http://slicehost.com">a new VPS on slicehost</a> and started using postfix. I followed <a href="http://www.howtoforge.com/virtual-users-and-domains-with-postfix-courier-mysql-and-squirrelmail-ubuntu-10.10">this great tutorial on HowToForge</a> (except for the squirrelMail part) to setup a mysql database with the vmail folders to store the mail. I couldn't get the Autoresponder in the tutorial to function correctly. Actually, it was 'eating' random mail, which was a weeks worth of headache in itself. So, we rolled out without any auto-response capabilities. 

I've been half-heartedly looking for another solution every few weeks, but haven't found anything other than a few Perl scripts (I'm not really famaliar with perl). So, yesterday I decided to write a ruby script to send auto-responses. I wanted to use text files to hold each autoresponse. Then, I'd just move them int and out of a folder to activate and deactivate them. I also took advantage of the 'new' folder within the vmail structure to reply to mail newer than the autoresponder config file.

The format of the config files is:
<pre>
email_address_to_respond_from

subject of response

message of response
</pre>

The message can be multiple lines until the end of the file.

For each config file in the directory, the script parses the file for the above information. Then it will check that user's new mail folder for files. Any new mail file which was modified (sent) after the modification date of the config file is parsed to get the sender's address(es)*. A new e-mail is composed using <a href="https://github.com/benprew/pony">benprew's pony gem</a> and sent to each of the senders. Finally, the script 'touches' the config file to move the modification date newer than the messages for which it just responded.

The nifty parts of the script are iterating over a directory listing of files:
<pre lang="ruby">Dir.new(directory_path).each { |filename| puts filename }</pre>
and using the <a href="http://www.ruby-doc.org/core/classes/File/Stat.html#M000088">stat method</a> of a file object to get the modified dateTime:
<pre lang="ruby">file.stat.mtime</pre>
and lastly, using the FileUtils module to 'touch' a file:
<pre lang="ruby">FileUtils.touch "#{file_path}/#{file_name}"</pre>

Here's the full source:

{{< gist 827900 >}}

-- Chris
